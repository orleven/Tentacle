#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import traceback
from lib.core.env import *
import asyncio
import async_timeout
import asyncssh
from lib.api.dnslog import dnslog_hander
from copy import deepcopy
from lib.core.g import task_name
from lib.core.model import Vul
from lib.util.util import get_time
from lib.util.util import output_excal
from lib.util.util import output_json
from script import BaseScript
from lib.core.g import log
from lib.core.g import conf
from lib.engine import BaseEngine
from lib.core.enums import EngineType
from lib.core.enums import ServicePortMap
from lib.core.enums import TargetStatus
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import ClientPayloadError
from lib.register.targetregister import TargetRegister
from lib.register.scriptregister import ScriptRegister
from lib.core.asyncpool import PoolCollector
from lib.util.interactshutil import Interactsh

class VulEngine(BaseEngine):

    def __init__(self):
        super().__init__()

       # Engine 属性
        self.engine_type = EngineType.VUL_ENGINE

        # self.target_queue = asyncio.Queue()
        self.port_queue = asyncio.Queue()
        self.ping_queue = asyncio.Queue()
        self.vul_queue = asyncio.Queue()
        # self.fingerprint_queue = asyncio.Queue()
        self.data_queue = asyncio.Queue()
        self.vul_dnslog_recode_map = {}
        self.dnslog_recode_list = []
        self.data_list = []
        self.interactsh_client = Interactsh()

    async def dnslog_center(self, manager: PoolCollector):
        async for dnslog_recode in dnslog_hander(self.interactsh_client):
            (target, data) = self.vul_dnslog_recode_map.get(dnslog_recode, None)
            if data:
                if dnslog_recode not in self.dnslog_recode_list:
                    self.dnslog_recode_list.append(dnslog_recode)
                    await self.data_queue.put((target, data))

    async def do_scan(self, queue: asyncio.Queue, target, module: BaseScript, func_name, parameter):
        host = target.get("host", None)
        port = target.get("port", None)
        name = module.__name__ if module else None
        try:
            if hasattr(module, "Script"):
                script = module.Script()
                if hasattr(script, func_name):
                    await script.initialize(target, parameter)
                    script.load_dict()
                    host = script.host
                    port = script.port
                    log.debug(f"Started running {name}:{func_name} for {host}:{port}...")
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
                            if script.dnslog:
                                self.vul_dnslog_recode_map[script.dnslog] = (target, data)
                            else:
                                await queue.put((target, data))
                    log.debug(f"Stoped running {name}:{func_name} for {host}:{port}")
                else:
                    log.error(f"Error, module: {name}:{func_name} address: {host}:{port}, error: function is exist")
        except (ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError, BrokenPipeError,
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
                    if target.get("status") not in [TargetStatus.INIT, TargetStatus.PINGSCAN] and target.get("port_connect", None) is False:
                        continue
                    if data:
                        await self.data_queue.put((target, data))
                    target["status"] = TargetStatus.VULSCAN
                    service = target["service"]
                    async for script in sr.load_script():
                        if target["port"]:
                            if service and service != ServicePortMap.UNKNOWN[0]:
                                if service != script.Script().service_type[0] and service != ServicePortMap.WEB[0]:
                                    continue
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
                    if not conf.scan.skip_port_scan:
                        await self.data_queue.put((target, data))
                        tr = TargetRegister()
                        if target["port"]:
                            target["status"] = TargetStatus.PORTSCAN
                            await manager.submit(self.do_scan, self.vul_queue, target, script, func_name=sr.func_name, parameter=sr.parameter)
                        else:
                            async for target in tr.load_target_by_target(target):
                                if target["port"]:
                                    target["status"] = TargetStatus.PORTSCAN
                                    await manager.submit(self.do_scan, self.vul_queue, target, script, func_name=sr.func_name, parameter=sr.parameter)
                    else:
                        await self.vul_queue.put((target, None))

        except Exception as e:
            log.error(str(e))
        finally:
            await manager.shutdown()

    async def ping_scan_submit_task(self, manager: PoolCollector):
        try:
            sr = ScriptRegister()
            script = sr.load_module_by_name("script.basic.ping_scan")
            while True:
                if self.ping_queue.empty():
                    await asyncio.sleep(0.1)
                else:
                    target, data = await self.ping_queue.get()
                    target["status"] = TargetStatus.PINGSCAN
                    if not conf.scan.skip_port_scan:
                        await manager.submit(self.do_scan, self.port_queue, target, script, func_name=sr.func_name, parameter=sr.parameter)
                    else:
                        await self.vul_queue.put((target, None))
        except Exception as e:
            log.error(str(e))
        finally:
            await manager.shutdown()

    async def init_scan_submit_task(self, manager: PoolCollector):
        try:
            tr = TargetRegister()
            if conf.scan.no_ping:
                async for target in tr.load_target_no_ping():
                    target["status"] = TargetStatus.INIT
                    if not conf.scan.skip_port_scan:
                        await self.port_queue.put((target, None))
                    else:
                        await self.vul_queue.put((target, None))

            else:
                async for target in tr.load_target_ping():
                    target["status"] = TargetStatus.INIT
                    await self.ping_queue.put((target, None))
            while True:
                if self.get_data_queue_size() == 0 and manager.scanning_task_count == 0 and manager.remain_task_count == 0:
                    await asyncio.sleep(conf.dnslog.dnslog_async_time + 5)
                    self.remaining_count = 0
                    self.scanning_count = 0
                    self.print_status()
                    await manager.shutdown()
                    break
                else:
                    await asyncio.sleep(3)
        except Exception as e:
            log.error(str(e))


    async def data_deal(self, manager: PoolCollector):
        try:
            await asyncio.sleep(3)
            while True:
                if self.data_queue.empty():
                    await asyncio.sleep(0.1)
                else:
                    target, data = await self.data_queue.get()
                    if data:
                        await self.print_data(data)
                        await self.save_data(data, Vul)
                        self.data_list.append(data)
        except Exception as e:
            log.error(str(e))
        finally:
            await manager.shutdown()

    def get_data_queue_size(self):
        """计算所有queue总和"""
        queue_num = self.port_queue.qsize() + self.vul_queue.qsize() + self.ping_queue.qsize()
        return queue_num

    async def print_data(self, result):
        self.found_count += 1
        address = result["url"] if result.get("url", None) else f'{result["host"]}:{result["port"]}' if result.get("port", None) else f'{result["host"]}'
        msg = f'[{result["script_path"]}] [{address}]: {result["detail"]}'
        log.success(msg)

    async def running(self):
        async with PoolCollector.create(num_workers=self.max_task_num) as manager:
            asyncio.ensure_future(self.init_scan_submit_task(manager))
            asyncio.ensure_future(self.ping_scan_submit_task(manager))
            asyncio.ensure_future(self.port_scan_submit_task(manager))
            # asyncio.ensure_future(self.fingerprint_scan_submit_task(manager))
            asyncio.ensure_future(self.vul_scan_submit_task(manager))
            asyncio.ensure_future(self.data_deal(manager))
            asyncio.ensure_future(self.heartbeat(manager))
            asyncio.ensure_future(self.dnslog_center(manager))
            async for result in manager.iter():
                self.scanned_count += 1

            if conf.basic.out:
                log.info(f'[{task_name}] Task export to {conf.basic.out}')
                output_excal(self.data_list, conf.basic.out)
            if conf.basic.out_csv:
                log.info(f'[{task_name}] Task export to {conf.basic.out_csv}')
                output_excal(self.data_list, conf.basic.out_csv)
            if conf.basic.out_json:
                log.info(f'[{task_name}] Task export to {conf.basic.out_json}')
                output_json(self.data_list, conf.basic.out_json)