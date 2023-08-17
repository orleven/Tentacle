#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven


from lib.core.env import *
import asyncio
from lib.core.g import task_name
from lib.core.g import conf
from lib.core.g import log
from lib.core.g import async_engine_sqlite_task
from lib.core.g import async_engine_sqlite_task_data
from lib.core.data import create_table
from lib.core.data import save_task
from lib.core.data import save_data
from lib.core.model import TaskBase
from lib.core.model import TaskDataBase
from lib.util.util import get_time
from lib.util.util import get_timestamp
from lib.core.asyncpool import PoolCollector
from lib.core.enums import EngineType
from lib.core.enums import TaskStatus

class BaseEngine(object):
    """
    Engine 基础类
    """

    def __init__(self):

        # Engine 属性
        self.engine_type = EngineType.BASE_ENGINE
        self.task_name = task_name
        self.task_status = TaskStatus.NONE

        # 属性初始化
        self.max_data_queue_num = conf.basic.max_data_queue_num
        self.max_task_num = conf.scan.max_task_num
        self.remaining_count = 0
        self.scanning_count = 0
        self.scanned_count = 0
        self.total_count = 0
        self.found_count = 0
        self.error_count = 0
        self.dnslog_api_key = conf.platform.dnslog_api_key
        self.timeout = conf.scan.scan_timeout

    def print_status(self):
        """打印状态"""

        self.total_count = self.scanned_count + self.scanning_count + self.remaining_count
        msg = f"[{task_name}] " \
            f"{self.found_count} found | {self.error_count} error | {self.remaining_count} remaining | " \
            f"{self.scanning_count} scanning | {self.scanned_count} scanned | {self.total_count} total. "
        log.info(msg)

    def get_data_queue_size(self):
        """计算所有queue总和"""

        return 0

    def do_scan(self, flow_hash, flow, addon):
        """虚函数，子类实现"""


    async def heartbeat(self, manager: PoolCollector):
        """注册引擎、心跳"""

        try:
            laster = get_time(0)
            while True:
                temp = get_time(get_timestamp() - 60)
                if temp > laster:
                    laster = get_time()
                    self.remaining_count = manager.remain_task_count
                    self.scanning_count = manager.scanning_task_count
                    self.print_status()

                    if conf.basic.debug:
                        for w in manager.pool.workers:
                            if w.is_running:
                                host = w.args[1].get("host", None)
                                port = w.args[1].get("port", None)
                                name = w.args[2].__name__
                                func_name = w.kwargs.get("func_name", None)
                                log.debug(f"Running {name}:{func_name} for {host}:{port}...")
                await asyncio.sleep(0.1)
        except Exception as e:
            log.error(str(e))
        finally:
            self.task_status = TaskStatus.STOP
            await manager.shutdown()


    async def running(self):
        """启动agent"""

        async with PoolCollector.create(num_workers=self.max_task_num) as manager:
            asyncio.ensure_future(self.heartbeat(manager))
            async for result in manager.iter():
                self.scanned_count += 1
                # if asyncio.isfuture(result) and result.result():
                #     yield result.result(), TaskDataBase
                # else:
                #     pass


    @property
    def task(self):
        return dict(task_name=self.task_name, engine=self.engine_type, status=self.task_status, value=conf.args)

    async def save_task(self, task_status):
        self.task_status = task_status
        key_update = dict(status=self.task_status, update_time=get_time())
        await save_task(async_engine_sqlite_task, self.task, key_update=key_update)

    async def print_data(self, result):
        """虚函数，子类实现"""

    async def save_data(self, result, result_type):
        key_update = dict(update_time=get_time())
        await save_data(async_engine_sqlite_task_data, result, result_type, key_update=key_update)

    async def run(self):
        await create_table(async_engine_sqlite_task, TaskBase)
        await self.save_task(TaskStatus.INIT)

        await create_table(async_engine_sqlite_task_data, TaskDataBase)
        await self.save_task(TaskStatus.RUN)

        await self.running()

        await self.save_task(TaskStatus.COMPLETE)

    def start(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.run())
        except:
            pass
