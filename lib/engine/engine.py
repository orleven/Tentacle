#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import os
import time
import asyncio
import traceback
import async_timeout
from typing import AsyncIterable
from typing import Iterable
from typing import Union
from lib.core.data import logger
from lib.core.data import paths
from lib.core.async_pool import PoolCollector
from lib.core.pocmanage import POCManager
from lib.core.database import TaskDataDB
from script import Script

class Engine(object):
    def __init__(self, name:str, targets: AsyncIterable, pm: POCManager, engine_name='Engine'):
        self.spend_time = 0
        self.name = name
        self.pm = pm
        self.engine_name = engine_name
        self.targets = targets
        self._total_task_count = 0
        self._error_task_count = 0
        self._find_task_count = 0
        self.interval_time = 60
        self.start_time = time.time()
        self.is_continue = True
        self.hashdb = TaskDataDB(os.path.join(paths.DATA_PATH, name))
        self.hashdb.connect()
        self.hashdb.init()

    def print_progress(self,manager: PoolCollector):
        found_count = self._find_task_count
        error_count = self._error_task_count
        remaining_count = manager.remain_task_count
        scanning_count = manager.scanning_task_count
        scanned_count = self._total_task_count - manager.remain_task_count
        total_count = self._total_task_count
        self.spend_time = time.time() - self.start_time
        msg = '[%s] %s found | %s error | %s remaining | %s scanning | %s scanned in %.2f seconds.(total %s)' % (
            self.name, found_count, error_count, remaining_count, scanning_count, scanned_count, self.spend_time,
            total_count)
        logger.sysinfo(msg)

    async def _progress_daemon(self, manager: PoolCollector):
        while True:
            await asyncio.sleep(self.interval_time)
            self.print_progress(manager)

    async def submit_task(self, manager: PoolCollector):
        """subclass should override this function for _submit_task"""

    async def do_scan(self, module: Script,target: Union[dict]) -> Iterable[dict]:
        """subclass should override this function for do_scan"""

    async def enum(self):
        """subclass should override this function for enum"""

  # async def brute_service_password(self, service_record: ServiceRecord):
    #     #
    #     # Web-WeakPassword
    #     #
    #     async with ClientSession() as session:
    #         if is_ipv6_address(service_record.host):
    #             host = f"[{service_record.host}]"
    #         else:
    #             host = service_record.host
    #         url_http = f"http://{host}:{service_record.port}/"
    #         url_https = f"https://{host}:{service_record.port}/"
    #         context = WebScanContext()
    #
    #         for _url in (url_http, url_https):
    #             req = HTTPRequest.from_url(_url)
    #             try:
    #                 async with req.send(session) as response:
    #                     await response.text()
    #                     http_flow = HTTPFlow(
    #                         request=req, response=HTTPResponse.from_aiohttp_response(response)
    #                     )
    #                     scanner: FormBrute = await self._pm.create('formbrute', session=session)
    #
    #                     async for record in scanner.handle(http_flow, context):
    #                         if record and isinstance(record, VulnRecord):
    #                             return [record]
    #             except Exception as e:
    #                 logger.warning(
    #                     "an error event happened when requesting the url:{}, exception:{}".format(
    #                         _url, e
    #                     )
    #                 )
    #                 continue
    #     return []
