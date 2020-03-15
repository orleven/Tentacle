#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import os
import argparse
from lib.utils.version import *
from lib.core.core import start
from lib.core.data import paths
from lib.utils.output import banner
from lib.core.init import initialize
from lib.core.settings import DESCRIPTION

def arg_set(parser):
    base = parser.add_argument_group('Base')
    base_target_group = base.add_mutually_exclusive_group()
    base_target_group.add_argument('-iS', "--target_simple",metavar='Target' ,type=str, default=None,help="Scan a single target (e.g. www.baidu.com)")
    base_target_group.add_argument('-iF', "--target_file",metavar='File', type=str, default=None,help='Load targets from targetFile (e.g. target.txt)')
    base_target_group.add_argument('-iN', "--target_network",metavar='IP/Mask', type=str, default=None,help='Generate IP from IP/MASK. (e.g. 192.168.111.0/24)')
    base_target_group.add_argument('-iX', "--target_nmap_xml", metavar='File', type=str, default=None,
                                   help='Load targets from nmap xml (e.g. nmap_res.xml)')
    base_target_group.add_argument('-iT', "--target_task", metavar='Task', type=str, default=None,
                                   help='Taskid (e.g. c81fc4f8f91ab191)')
    base_target_group.add_argument('-iE', "--target_search_engine", metavar='key', type=str, default=None,
                                   help='Load targets from baidu/bing/360so. (e.g. powered by discuz)')
    base_target_group.add_argument('-gg', "--target_google", metavar='key', type=str, default=None,
                                   help='Load targets from google. (e.g. intext:powered by discuz)')
    base_target_group.add_argument('-sd', "--target_shodan", metavar='key', type=str, default=None,
                                   help='Load targets from shodan  (e.g. apache)')
    base_target_group.add_argument('-ze', "--target_zoomeye", metavar='key', type=str, default=None,
                                   help='Load targets from zoomeye  (e.g. powered by discuz)')
    base_target_group.add_argument('-ff', "--target_fofa", metavar='key', type=str, default=None,
                                   help='Load targets from fofa  (e.g. app:weblogic)')

    port = parser.add_argument_group('Port')
    port.add_argument("-sP", "--skip_port_scan", action='store_true', help="Skip port scan", default=False)
    port.add_argument("-lP", "--limit_port_scan", action='store', help="Limit port scope scan, e.g 80-100,8080,top100,*", default=False)

    module = parser.add_argument_group('Module')
    module.add_argument("-m", "--module", help="Load script module", default=False, action='store')
    module.add_argument("-f", "--function", help="Load function of script module, e.g show,prove", default='prove', action='store')
    module.add_argument("-p", "--parameter", help="Load data for function of module, e.g. -p \"U=username.txt&P=password.txt\"", default=False, action='store')
    module.add_argument("--show", action='store_true', help="Show all poc scripts module", default=False)
    module.add_argument("-t", "--thread", type=int, help="Thread Num e.g. 100", default=100 ,action='store')

    other = parser.add_argument_group('Other')
    other.add_argument('-tS', "--task_show",  metavar='TaskID', type=str, default=None,help= 'Show task (e.g. all,c81fc4f8f9ab1902)')
    other.add_argument("-v", "--verbose", action='store_true', help="Show verbose", default=False)
    other.add_argument("-d", "--debug", action='store_true', help="Show debug info", default=False)
    other.add_argument("-o", "--out", type=str, help="Output file e.g res.xlsx", default=None)
    other.add_argument("--update", action='store_true', help="Update", default=False)
    other.add_argument("--help", help="Show help", default=False, action='store_true')
    return parser

def handle(parser):
    banner()
    args = parser.parse_args()
    paths.ROOT_PATH  = os.path.dirname(os.path.realpath(__file__))
    initialize(args)
    if args.help:
        parser.print_help()
    else:
        start(args)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION,formatter_class=argparse.RawTextHelpFormatter, add_help=False)
    parser = arg_set(parser)
    handle(parser)



