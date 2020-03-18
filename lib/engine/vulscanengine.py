#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import copy
import asyncio
import traceback
import async_timeout
from typing import Iterable
from typing import Union
from script import Script
from asyncio import TimeoutError
from typing import AsyncIterable
from lib.core.pocmanage import POCManager
from asyncio import CancelledError
from lib.core.enums import SERVICE_PORT_MAP
from lib.core.data import conf
from lib.core.data import logger
from lib.engine.engine import Engine
from lib.utils.output import print_dic
from lib.core.async_pool import PoolCollector
from lib.core.common import get_safe_ex_string

class VulScanEngine(Engine):
    def __init__(self, name:str, targets: AsyncIterable, pm: POCManager, engine_name=None):
        self.vul_modules = []
        self.info_modules = []
        self.vul_targets = asyncio.Queue()

        for module in pm.modules:
            if module.__name__ == 'script.info.port_scan':
                self.info_modules.append(module)
            else:
                self.vul_modules.append(module)

        if engine_name == None:
            engine_name = self.__class__.__name__
        super(VulScanEngine, self).__init__(name, targets, pm, engine_name)

    async def do_scan(self, module: Script,target: Union[dict]) -> Iterable[dict]:
        records = []
        func_name = self.pm.func_name
        parameter = self.pm.parameter
        flag = -1
        try:
            poc = module.POC()
            poc.initialize(target['host'], target['port'], target['url'], parameter)
            func = getattr(poc, func_name)
            logger.debug(
                "Running %s:%s for %s:%s" % (module.__name__, func_name, poc.target_host, poc.target_port))
            async with async_timeout.timeout(timeout=int(conf['basic']['timeout'])):
                await func()
                flag = poc.flag
                if poc.url != None:
                    target['url'] = poc.url
        except AttributeError as e:
            if 'has no attribute \'POC\'' in get_safe_ex_string(e):
                logger.error('Invalid POC script, Please check the script: %s' % module.__name__, )
            elif '\'POC\' object has no attribute' in get_safe_ex_string(e):
                logger.error('%s, Please check it in the script: %s' % (e, module.__name__))
            elif 'Function is not exist.' in get_safe_ex_string(e):
                logger.error(
                    'Function is not exist, Please check \'%s\' in the script: %s' % (
                        func_name, module.__name__,))
            else:
                self.errmsg = traceback.format_exc()
                logger.error(self.errmsg)
                logger.error("%s %s:%s for %s:%d" % (e, module.__name__, func_name, target['host'], target['port']))
            self._error_task_count += 1
        except KeyError as e:
            logger.error("Missing parameters: %s, please load parameters by -p. For example. -p %s=value" % (
                e, str(e).replace('\'', '')))
            self._error_task_count += 1
        except (ConnectionResetError, ConnectionAbortedError, TimeoutError):
            flag = poc.flag
        except (CancelledError, ConnectionRefusedError, OSError):
            if target['status'] != None:
                target['status'] -= 1
            else:
                target['status'] = -1
        except Exception:
            self._error_task_count += 1
            errmsg = traceback.format_exc()
            logger.error("Error for " + target['host'] + ":" + str(target['port']) + "\r\n"+ errmsg)
        finally:
            if conf.VERBOSE or flag >= 0:
                if poc.flag >= 0:
                    self._find_task_count += 1
                    if module.__name__ == 'script.info.port_scan':
                        target['status'] = 5
                        if  len(poc.res) == 0 :
                            poc.res = [{"info": None , "key": "port scan"}]
                        for res in poc.res:
                            target['service'] = res['info']
                            await self.vul_targets.put(target)
                    else:
                        target['status'] = 3
                data = {
                    "id": target['id'],
                    "flag": poc.flag,
                    'module_name': module.__name__,
                    'func_name': func_name,
                    'target_host': poc.target_host,
                    'target_port': poc.target_port,
                    'url': poc.url,
                    'base_url': poc.base_url,
                    "req": poc.req,
                    "res": poc.res,
                    "other": poc.other,
                }
                self.hashdb.insert(data)
                self.hashdb.flush()
                print_dic(data)
                records.append(data)
            logger.debug("Ending  %s:%s for %s:%s" % (module.__name__, func_name, poc.target_host, poc.target_port))
        return records

    async def _port_scan_submit_task(self, manager: PoolCollector):
        try:
            id = 0
            async for target in self.targets:
                id += 1
                for module in self.info_modules:
                    poc = module.POC()
                    _ = {'id': id, 'status': 3}
                    for key, value in target.items():
                        _[key] = value
                    if target['port'] is None:
                        if isinstance(poc.service_type[1], list):
                            for port in poc.service_type[1]:
                                temp = copy.deepcopy(_)
                                temp['port'] = port
                                temp['service'] = poc.service_type[0]
                                self._total_task_count += 1
                                await manager.submit(self.do_scan, module, temp)
                        else:
                            _['port'] = poc.service_type[1]
                            _['service'] = poc.service_type[0]
                            self._total_task_count += 1
                            await manager.submit(self.do_scan, module, _)
                    else:
                        self._total_task_count += 1
                        await manager.submit(self.do_scan, module, _)
        except Exception as e:
            errmsg = traceback.format_exc()
            logger.error(errmsg)
        finally:
            while True:
                if manager.is_finished:
                    self.is_continue = False
                await asyncio.sleep(1)

    async def _vul_scan_submit_task(self, manager: PoolCollector):
        try:
            while True:
                if not self.vul_targets.empty():
                    target = await self.vul_targets.get()
                    for module in self.vul_modules:
                        if target['status'] is None or target['status'] < 0:
                            break
                        if target['service'] is not None and target['service'] != SERVICE_PORT_MAP.UNKNOWN[0]:
                            if target['service'] in [SERVICE_PORT_MAP.WEB[0], SERVICE_PORT_MAP.HTTP[0], SERVICE_PORT_MAP.HTTPS[0]]:
                                if module.POC().service_type[0] not in SERVICE_PORT_MAP.WEB_LIST:
                                    continue
                            elif target['service'] != module.POC().service_type[0]:
                                continue
                        self._total_task_count += 1
                        await manager.submit(self.do_scan, module, target)
                elif not self.is_continue:
                    break
                else:
                    await asyncio.sleep(0.1)

        except Exception as e:
            errmsg = traceback.format_exc()
            logger.error(errmsg)
        finally:
            await manager.shutdown()

    async def _skip_and_vul_scan_submit_task(self, manager: PoolCollector):
        try:
            id = 0
            async for target in self.targets:
                id += 1
                for module in self.vul_modules:
                    poc = module.POC()
                    _ = {'id': id, 'status': 3}
                    for key, value in target.items():
                        _[key] = value
                    if target['port'] is None:
                        if isinstance(poc.service_type[1], list):
                            for port in poc.service_type[1]:
                                temp = copy.deepcopy(_)
                                temp['port'] = port
                                temp['service'] = poc.service_type[0]
                                self._total_task_count += 1
                                await manager.submit(self.do_scan, module, temp)
                        else:
                            _['port'] = poc.service_type[1]
                            _['service'] = poc.service_type[0]
                            self._total_task_count += 1
                            await manager.submit(self.do_scan, module, _)
                    else:
                        self._total_task_count += 1
                        await manager.submit(self.do_scan, module, _)
        except Exception as e:
            errmsg = traceback.format_exc()
            logger.error(errmsg)
        finally:
            await manager.shutdown()


    async def enum(self):
        logger.sysinfo("Running task: %s"% self.name)
        async with PoolCollector.create(num_workers=conf['thread_num']) as manager:
            asyncio.ensure_future(self._progress_daemon(manager))
            if conf['skip_port_scan']:
                asyncio.ensure_future(self._skip_and_vul_scan_submit_task(manager))
            else:
                asyncio.ensure_future(self._port_scan_submit_task(manager))
                asyncio.ensure_future(self._vul_scan_submit_task(manager))

            async for record in manager.iter():
                if asyncio.isfuture(record):
                    for record in record.result():
                        yield record
                else:
                    yield record
            self.print_progress(manager)