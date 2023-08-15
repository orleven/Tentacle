#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import traceback
from lib.core.env import *
import asyncio
import async_timeout
import asyncssh
from copy import deepcopy
from lib.core.g import task_name
from lib.core.model import Vul
from lib.util.util import get_time, output_excal
from script import BaseScript
from lib.core.g import log
from lib.core.g import conf
from lib.engine import BaseEngine
from lib.core.enums import EngineType
from lib.core.enums import TargetStatus
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import ClientPayloadError
from lib.register.targetregister import TargetRegister
from lib.register.scriptregister import ScriptRegister
from lib.core.asyncpool import PoolCollector

class VulEngine(BaseEngine):

    def __init__(self):
        super().__init__()

       # Engine 属性
        self.engine_type = EngineType.VUL_ENGINE

        # self.target_queue = asyncio.Queue()
        self.port_queue = asyncio.Queue()
        self.vul_queue = asyncio.Queue()
        # self.fingerprint_queue = asyncio.Queue()
        self.data_queue = asyncio.Queue()

    async def do_scan(self, queue: asyncio.Queue, target, module: BaseScript, func_name, parameter):
        host = target.get("host", None)
        port = target.get("port", None)
        name = module.__name__ if module else None
        try:
            name = module.__name__
            if hasattr(module, "Script"):
                script = module.Script()
                if hasattr(script, func_name):
                    await script.initialize(target, parameter)
                    script.load_dict()
                    host = script.host
                    port = script.port
                    # log.debug(f"Started running {name}:{func_name} for {host}:{port}...")
                    function = getattr(script, func_name)
                    async with async_timeout.timeout(delay=conf.scan.scan_timeout):
                        async for result in function():
                            target = script.get_target()
                            if result:
                                data = dict(
                                    task_name=task_name, url=script.url, detail=str(result), scheme=script.protocol,
                                    script_name=script.name, script_path=script.script_path, update_time=get_time(),
                                    host=script.host, port=script.port,
                                )
                            else:
                                data = None
                            if name == "script.basic.port_scan":
                                await queue.put((target, data))
                            # elif name == "script.basic.fingerprint_scan":
                            #     await queue.put((target, data))
                            else:
                                await queue.put((target, data))

                            if data:
                                return data
                    # log.debug(f"Stoped running {name}:{func_name} for {host}:{port}")
                else:
                    log.error(f"Error, module: {name}:{func_name} address: {host}:{port}, error: function is exist")
        except (ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError,
                TimeoutError, ClientPayloadError, RuntimeError, BrokenPipeError, OSError,
                asyncssh.Error):
            self.error_count += 1
        except Exception as e:
            log.error(traceback.format_exc())
            log.error(f"Error, module: {name}:{func_name} address: {host}:{port}, error: {str(e)}")
            self.error_count += 1


    async def vul_scan_submit_task(self, manager: PoolCollector):
        try:
            sr = ScriptRegister()
            await sr.load_module()
            while True:
                if self.vul_queue.empty():
                    await asyncio.sleep(0.1)
                else:
                    target, data = await self.vul_queue.get()
                    if target.get("status") != TargetStatus.INIT and not target.get("ping", False):
                        continue
                    if data:
                        await self.data_queue.put((target, data))
                    target["status"] = TargetStatus.VULSCAN
                    async for script in sr.load_script():
                        if target["port"]:
                            await manager.submit(self.do_scan, self.data_queue, target, script, func_name=sr.func_name, parameter=sr.parameter)
                        else:
                            for port in script.Script().service_type[1]:
                                temp_target = deepcopy(target)
                                temp_target["port"] = port
                                await manager.submit(self.do_scan, self.data_queue, temp_target, script, func_name=sr.func_name, parameter=sr.parameter)
        except Exception as e:
            log.error(str(e))
        finally:
            await manager.shutdown()

    async def port_scan_submit_task(self, manager: PoolCollector):
        try:
            sr = ScriptRegister()
            script = sr.load_module_by_name("script.basic.port_scan")
            while True:
                if self.port_queue.empty():
                    await asyncio.sleep(0.1)
                else:
                    target, data = await self.port_queue.get()
                    target["status"] = TargetStatus.PORTSCAN
                    await manager.submit(self.do_scan, self.vul_queue, target, script, func_name=sr.func_name, parameter=sr.parameter)
        except Exception as e:
            log.error(str(e))
        finally:
            await manager.shutdown()

    async def init_scan_submit_task(self, manager: PoolCollector):
        try:
            tr = TargetRegister()
            async for target in tr.load_target():
                target["status"] = TargetStatus.INIT
                if target["port"] and not conf.scan.skip_basic_scan:
                    await self.port_queue.put((target, None))
                else:
                    await self.vul_queue.put((target, None))

            while True:
                if self.get_data_queue_size() == 0 and manager.scanning_task_count == 0 and manager.remain_task_count == 0:
                    self.remaining_count = 0
                    self.scanning_count = 0
                    self.print_status()
                    await manager.shutdown()
                    break
                else:
                    await asyncio.sleep(3)
        except Exception as e:
            log.error(str(e))

    # async def fingerprint_scan_submit_task(self, manager: PoolCollector):
    #     try:
    #         sr = ScriptRegister()
    #         script = sr.load_module_by_name("script.basic.fingerprint_scan")
    #         while True:
    #             if self.fingerprint_queue.empty():
    #                 await asyncio.sleep(0.1)
    #             else:
    #                 target, data = await self.fingerprint_queue.get()
    #                 await self.data_queue.put((target, data))
    #                 if target.get("status") != TargetStatus.INIT and not target.get("ping", False):
    #                     continue
    #                 target["status"] = TargetStatus.FINGERPRINTSCAN
    #                 if script:
    #                     await manager.submit(self.do_scan, self.vul_queue, target, script, func_name=sr.func_name, parameter=sr.parameter)
    #                 else:
    #                     await self.vul_queue.put((target, data))
    #     except Exception as e:
    #         log.error(str(e))
    #     finally:
    #         await manager.shutdown()

    async def data_deal(self, manager: PoolCollector):
        try:
            await asyncio.sleep(3)
            while True:
                if self.data_queue.empty():
                    await asyncio.sleep(0.1)
                else:
                    target, data = await self.data_queue.get()
                    await self.print_data(data)
                    await self.save_data(data, Vul)
        except Exception as e:
            log.error(str(e))
        finally:
            await manager.shutdown()

    def get_data_queue_size(self):
        """计算所有queue总和"""
        # queue_num = self.port_queue.qsize() + self.fingerprint_queue.qsize() + self.vul_queue.qsize()
        queue_num = self.port_queue.qsize() + self.vul_queue.qsize()
        return queue_num

    async def print_data(self, result):
        self.found_count += 1
        address = result["url"] if result.get("url", None) else f'{result["host"]}:{result["port"]}'
        msg = f'[{result["script_path"]}] [{address}]: {result["detail"]}'
        log.success(msg)

    async def running(self):
        async with PoolCollector.create(num_workers=self.max_task_num) as manager:
            asyncio.ensure_future(self.init_scan_submit_task(manager))
            asyncio.ensure_future(self.vul_scan_submit_task(manager))
            asyncio.ensure_future(self.port_scan_submit_task(manager))
            # asyncio.ensure_future(self.fingerprint_scan_submit_task(manager))
            asyncio.ensure_future(self.data_deal(manager))
            asyncio.ensure_future(self.heartbeat(manager))

            data_list = []
            async for result in manager.iter():
                self.scanned_count += 1
                if asyncio.isfuture(result):
                    if result.result():
                        data_list.append(result.result())
            if conf.basic.out:
                log.info(f'[{task_name}] Task export to {conf.basic.out}')
                output_excal(data_list, conf.basic.out)