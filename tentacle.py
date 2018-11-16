#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import os
import sys
import logging
import argparse
from lib.utils.output import banner
from lib.core.core import normal
# from lib.core.core import server
# from lib.core.core import client
# from lib.core.settings import RESTAPI_DEFAULT_PORT
# from lib.core.settings import RESTAPI_DEFAULT_HOST
# from lib.core.settings import RESTAPI_DEFAULT_ADAPTER
from lib.core.init import set_paths



# Don't write pyc
sys.dont_write_bytecode = True

# Python version check
try:
    __import__("lib.utils.version")
except ImportError:
    exit("[!] wrong installation detected (missing modules). Visit 'https://' for further details")


def arg_set(parser):
    base = parser.add_argument_group('Base')
    base_mode_group = base.add_mutually_exclusive_group()
    base_mode_group.add_argument("-n", "--normal", help="Act as a normal model", default=False, action='store_true')
    # base_mode_group.add_argument("-s", "--server", help="Act as a REST-JSON API server model", default=False, action='store_true')
    # base_mode_group.add_argument("-c", "--client", help="Act as a REST-JSON API client model", default=False, action='store_true')
    # base.add_argument("-u", "--url", type=str, help="The target e.g http://www.baidu.com", default=None, action="store")
    # base.add_argument("-th", "--target_host", type=str, help="The target host e.g 127.0.0.1", default=None, action="store")
    # base.add_argument("-tp", "--target_port", type=str, help="The target port e.g 127.0.0.1", default=None, action="store")

    base_target_group = base.add_mutually_exclusive_group()
    base_target_group.add_argument('-iS', "--target_simple",metavar='Target' ,type=str, default=None,help="Scan a single target (e.g. www.baidu.com)")
    base_target_group.add_argument('-iF', "--target_file",metavar='File', type=str, default=None,help='Load targets from targetFile (e.g. target.txt)')
    base_target_group.add_argument('-iN', "--target_network",metavar='IP/Mask', type=str, default=None,help='Generate IP from IP/MASK. (e.g. 192.168.111.0/24)')
    base_target_group.add_argument('-iT', "--target_task", metavar='Task', type=str, default=None,
                                   help='Taskid (e.g. c81fc4f8f91ab191)')
    base_target_group.add_argument('-sE', "--target_search_engine", metavar='key', type=str, default=None,
                                   help='Load targets from search engine,such as baidu/bing/google/360so. (e.g. powered by discuz)')
    # base_target_group.add_argument('-sS', "--target_shodan", metavar='key', type=str, default=None,
    #                                help='Load targets from shodan')
    # base_target_group.add_argument('-sZ', "--target_zoomeye", metavar='key', type=str, default=None,
    #                                help='Load targets from zoomeye')
    base.add_argument('-iP', "--target_port",metavar='Port', type=int, default=None,help='Generate port  (e.g. 80)')

    # mode = parser.add_argument_group('Mode')
    # mode.add_argument("-p", "--port", help="Port of the the REST-JSON API server (default %d)" % RESTAPI_DEFAULT_PORT, default=RESTAPI_DEFAULT_PORT, type=int, action='store')
    # mode.add_argument("-h", "--host", help="Host of the the REST-JSON API server (default %s)" % RESTAPI_DEFAULT_HOST, default=RESTAPI_DEFAULT_HOST, type=str, action='store')
    # mode.add_argument("--adapter", help="Server (bottle) adapter to use (default \"%s\")" % RESTAPI_DEFAULT_ADAPTER,default=RESTAPI_DEFAULT_ADAPTER, action="store")
    # mode.add_argument("--username", type=str, help="Basic authentication username (optional)", action="store")
    # mode.add_argument("--password", type=str, help="Basic authentication username (optional)", action="store")

    module = parser.add_argument_group('Module')
    module.add_argument("-m", "--module", help="Load script module", default=False, action='store')
    module.add_argument("-f", "--function", help="Load function of script module, e.g show,prove", default=False, action='store')
    module.add_argument("--show", action='store_true', help="Show all poc scripts module", default=False)
    module.add_argument("--thread", type=int, help="Thread Num e.g. 100", default=20 ,action='store')
    # module.add_argument("--parameter", help="Load data for function of module, e.g. --parameter 'password=redispass'", default=False, action='store')

    # burst = parser.add_argument_group('Burst')
    # burst.add_argument('-d1', "--dic_one", metavar='File', type=str, default=None,help='load dictionary from targetFile (e.g. ./data/dic1.txt)')
    # burst.add_argument('-d2', "--dic_two", metavar='File', type=str, default=None,help='load dictionary from targetFile (e.g. ./data/dic2.txt)')
    # burst.add_argument('-dM', "--dic_mode", metavar='Mode', type=int, default=1,help='load dictionary mode, 1 is cluster bomb(n*n),2 is pitchfork(n)')

    other = parser.add_argument_group('Other')
    other.add_argument("--help", help="Show help", default=False, action='store_true')
    other.add_argument("-v", "--verbose", action='store_true', help="Show verbose", default=False)
    other.add_argument("-d", "--debug", action='store_true', help="Show debug info", default=False)
    other.add_argument('-tS',"--task_show",  metavar='TaskID', type=str, default=None,help='Show task (e.g. all,c81fc4f8f9ab1902)')
    other.add_argument("-o", "--out", type=str, help="Output file e.g res.txt", default=None)
    other.add_argument("--update", action='store_true', help="Update", default=False)
    # other.add_argument("--config", type=str, help="Load config file", default=None)

    # Mark
    # parser.add_argument("-k", "--key", type=str, help="The order key e.g. title、status、host", default="id")
    # parser.add_argument("-t", "--timeout", type=str, help="Timeout", default="3")
    # parser.add_argument("-f", "--file",type=str, help="Load ip dictionary e.g. 192.168.1.2:8080", default=None)
    # parser.add_argument("-s", "--search",type=str, help="search key in title or content,e.g. 管理,后台", default=None)

    return parser

def handle(parser):
    # Initialize paths
    set_paths(os.path.dirname(os.path.realpath(__file__)))

    # Print banner
    banner()

    args = parser.parse_args()

    if args.help:
        parser.print_help()
    # elif args.server :
    #     server(args.host, args.port, adapter=args.adapter, username=args.username, password=args.password)
    # elif args.client:
    #     client(args.host, args.port, username=args.username, password=args.password)
    elif args.normal:
        normal(args)
    else:
        parser.print_help()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Tentacle', epilog='Tentacle',formatter_class=argparse.RawTextHelpFormatter, add_help=False)
    parser = arg_set(parser)
    handle(parser)

