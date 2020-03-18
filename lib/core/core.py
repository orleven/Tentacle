#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import ssl
import sys
import asyncio
from lib.core.common import random_MD5
from lib.core.options import init_options
from lib.core.data import paths
from lib.core.data import conf
from lib.core.data import logger
from lib.core.database import TaskDB
from lib.core.enums import TASK_STATUS
from lib.core.common import get_time
from lib.utils.output import output_excal
from lib.core.pocmanage import POCManager
from lib.core.targetmanager import TargetManager
from lib.engine.vulscanengine import VulScanEngine

SSL_PROTOCOLS = (asyncio.sslproto.SSLProtocol,)
try:
    import uvloop.loop
except ImportError:
    pass
else:
    SSL_PROTOCOLS = (*SSL_PROTOCOLS, uvloop.loop.SSLProtocol)


def start(args):
    name = random_MD5()[8:-8]
    logger.sysinfo("Created task: %s" % name)
    init_options(args)
    database = TaskDB(paths.DATABASE_PATH)
    database.connect()
    database.init()
    database.insert_task(name, args, TASK_STATUS.TASK_INIT_STATUS, get_time())
    tm = TargetManager(args)
    pm = POCManager(args.module, args.function, args.parameter)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ignore_aiohttp_ssl_eror(loop)
    database.update_task_status(name, TASK_STATUS.TASK_RUN_STATUS, get_time())
    try:
        loop.run_until_complete(scan(name, tm, pm))
    except KeyboardInterrupt:
        pass
    database.update_task_status(name, TASK_STATUS.TASK_COMPLETE_STATUS, get_time())

async def scan(name, tm, pm):
    pm.load()
    targets = tm.load()
    engine = VulScanEngine(name, targets, pm)
    results = []
    async for result in engine.enum():
        results.append(result)

    if conf.OUT:
        output_excal(results, conf.OUT, name)


    # if True:
    #     results = []
    #     port_pm = POCManager(os.path.join('script', 'info', 'port_scan'), args.function, args.parameter)
    #     port_pm.load()
    #     engine = ServiceScanEngine(name, targets, port_pm)
    #     async for result in engine.enum():
    #         results.append(result)
    #     targets = tm.load_from_list(results)
    #
    # engine = ServiceVulnEngine(name, targets, pm)
    # async for result in engine.enum():
    #     pass

def ignore_aiohttp_ssl_eror(loop):
    if sys.version_info >= (3, 7, 4):
        return

    orig_handler = loop.get_exception_handler()

    def ignore_ssl_error(loop, context):

        if context.get("message") in {
            "SSL handshake failed",
            "SSL error in data received",
            "Fatal error on transport",
        }:
            # validate we have the right exception, transport and protocol
            exception = context.get('exception')
            protocol = context.get('protocol')
            if isinstance(exception, ssl.SSLError) and isinstance(protocol, SSL_PROTOCOLS):
                if exception.reason == 'WRONG_VERSION_NUMBER':
                    logger.debug('Ignoring asyncio SSL WRONG_VERSION_NUMBER error')
                elif exception.reason == 'KRB5_S_INIT':
                    """Ignore aiohttp #3535 / cpython #13548 issue with SSL data after close

                        There is an issue in Python 3.7 up to 3.7.3 that over-reports a
                        ssl.SSLError fatal error (ssl.SSLError: [SSL: KRB5_S_INIT] application data
                        after close notify (_ssl.c:2609)) after we are already done with the
                        connection. See GitHub issues aio-libs/aiohttp#3535 and
                        python/cpython#13548.

                        Given a loop, this sets up an exception handler that ignores this specific
                        exception, but passes everything else on to the previous exception handler
                        this one replaces.

                        Checks for fixed Python versions, disabling itself when running on 3.7.4+
                        or 3.8.
                        """
                    logger.debug('Ignoring asyncio SSL KRB5_S_INIT error')
                return

        if orig_handler is not None:
            orig_handler(loop, context)
        else:
            loop.default_exception_handler(context)

    loop.set_exception_handler(ignore_ssl_error)
