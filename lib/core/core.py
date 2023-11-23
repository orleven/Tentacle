#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import ssl
import asyncio
from lib.core.env import *
from lib.core.g import log
from lib.core.g import conf
from attribdict import AttribDict
from lib.core.enums import CustomLogging
from lib.engine.vulengine import VulEngine
from lib.register.scriptregister import ScriptRegister
from lib.register.targetregister import TargetRegister
from lib.util.updateutil import update_program
from lib.util.util import serialize_object

SSL_PROTOCOLS = (asyncio.sslproto.SSLProtocol, )
try:
    import uvloop.loop
except ImportError:
    pass
else:
    SSL_PROTOCOLS = (*SSL_PROTOCOLS, uvloop.loop.SSLProtocol)

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
                    log.debug('Ignoring asyncio SSL WRONG_VERSION_NUMBER error')
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
                    log.debug('Ignoring asyncio SSL KRB5_S_INIT error')
                return

        if orig_handler is not None:
            orig_handler(loop, context)
        else:
            loop.default_exception_handler(context)

    loop.set_exception_handler(ignore_ssl_error)

def load_dict():
    ad = AttribDict()
    for parent, dirnames, filenames in os.walk(conf.scan.scan_dict_path, followlinks=True):
        for each in filenames:
            if '.txt' in each:
                file_path = os.path.join(parent, each)
                name = each
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as f:
                        ad[name] = [line.replace('\r', '').replace('\n', '').strip().rstrip() for line in f.readlines()]
                else:
                    log.error("File is not exist: %s" % file_path)
    return ad

def handle_options(args):
    """参数解析与配置"""

    if hasattr(args, "test") and args.test:
        conf.basic.test = True
    else:
        conf.basic.test = False

    if hasattr(args, "thread") and args.thread:
        conf.scan.max_task_num = args.thread

    # target
    conf.scan.simple = args.target_simple
    conf.scan.file = args.target_file
    conf.scan.nmap_xml = args.target_nmap_xml
    conf.scan.task = args.target_task
    conf.scan.search_engine = args.target_search_engine
    conf.scan.zoomeye = args.target_zoomeye
    conf.scan.shodan = args.target_shodan
    conf.scan.fofa = args.target_fofa
    conf.scan.google = args.target_google

    # port
    conf.scan.skip_port_scan = args.skip_port_scan
    conf.scan.limit_port_scan = args.limit_port_scan

    # module
    conf.scan.module = args.module
    conf.scan.exclude_module = args.exclude_module
    conf.scan.parameter = args.parameter
    conf.scan.function = args.function

    # ping
    conf.scan.no_ping = args.no_ping

    conf.scan.scan_dict = load_dict()

    conf.basic.out = args.out
    conf.basic.out_csv = args.out_csv
    conf.basic.out_json = args.out_json
    if conf.basic.out:
        filename = conf.basic.out if '.xlsx' in conf.basic.out else conf.basic.out + '.xlsx'
        conf.basic.out = os.path.join(OUTPUT_PATH, filename)
    if conf.basic.out_csv:
        filename = conf.basic.out_csv if '.xlsx' in conf.basic.out_csv else conf.basic.out_csv + '.xlsx'
        conf.basic.out_csv = os.path.join(OUTPUT_PATH, filename)
    if conf.basic.out_json:
        filename = conf.basic.out_json if '.json' in conf.basic.out_json else conf.basic.out_json + '.json'
        conf.basic.out_json = os.path.join(OUTPUT_PATH, filename)

    conf.basic.debug = args.debug
    if conf.basic.debug:
        log_level = CustomLogging.DEBUG
        log.set_level(log_level)
        log.debug(f"Setting {PROJECT_NAME} debug mode...")

    if args.show:
        sr = ScriptRegister()
        sr.show()
        sys.exit(0)

    if args.task_show:
        tr = TargetRegister()
        tr.start_print(args.task_show)
        sys.exit(0)

    if args.update:
        update_program()
        sys.exit(0)

    conf.args = serialize_object(args)

def initialize():
    log.debug(f"Initialize {PROJECT_NAME} path...")
    path_list = [LOG_PATH, DATA_PATH, TOOL_PATH, CONFIG_PATH, OUTPUT_PATH, SCRIPT_PATH, DICT_PATH]
    for path in path_list:
        if not os.path.exists(path):
            os.mkdir(path)

    log.debug(f"Initialize {PROJECT_NAME} db...")


def start(args):
    """开启agent端"""

    initialize()
    handle_options(args)
    log.info(f"Created task ...")
    ms = VulEngine()

    try:
        log.info(f"Starting task...")
        ms.start()
    except KeyboardInterrupt:
        log.info(f"Ctrl C - stopping task!")
    except Exception as e:
        log.critical(f"Error run task, error: {str(e)}")