#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import re
import os
import sys
import glob
from lib.utils.output import print_dic
from lib.core.common import unserialize_object
from lib.core.hashdb import HashDB
from lib.core.database import Database
from lib.core.data import logger
from lib.core.data import conf
from lib.core.data import paths
from lib.utils.output import output_excal


def init_options(args):

    conf.VERBOSE = args.verbose
    conf.OUT = args.out

    show_task(args)
    module_register(args)
    function_register(args)
    engine_register(args)
    target_register(args)
    parameter_register(args)


def function_register(args):

    if args.function:
        conf['func_name'] = args.function
    else:
        conf['func_name'] = 'prove'

    logger.debug("Set function: %s" % conf['func_name'])

def parameter_register(args):

    if args.parameter:
        try:
            datas = args.parameter.split('&')
            dic = {}
            for _data in datas:
                _key, _value = _data.split('=')
                dic[_key] = _value
            logger.debug("Set parameter: %s." % str(dic))
        except :
            msg = 'The parameter input error, please check your input e.g. -p "userlist=user.txt", and you should make sure the module\'s function need the parameter. '
            sys.exit(logger.error(msg))



def engine_register(args):

    if  not 0 < args.thread < 501:
        msg = 'Invalid input in [-t] for thread num, range: 1 to 500.'
        sys.exit(logger.error(msg))

    conf['thread_num'] = args.thread
    logger.debug("Set thread: %s." % str(conf['thread_num']))

def module_register(args):
    _len = len(paths.ROOT_PATH) + 1
    if args.show:
        msg = 'There are available modules as follows: \r\n'
        msg += '------------------------------------------------------\r\n'
        msg += '| {: <50} |\r\n'.format('Module and path,you can load module by -m ')
        msg += '------------------------------------------------------\r\n'
        for parent, dirnames, filenames in os.walk(paths.SCRIPT_PATH, followlinks=True):
            for each in filenames:
                if '__init__' in each:
                    continue
                file_path = os.path.join(parent, each)
                msg += '| {: <50} |\r\n'.format(file_path[_len:-3])
        msg += '------------------------------------------------------\r\n'
        sys.exit(logger.sysinfo(msg))

    input_module = args.module
    if not input_module:
        msg = 'Use -m to load module. Example: [-m test] or [-m ./script/test.py] or [-m @thinkphp], and you can see all module name by --show.'
        sys.exit(logger.error(msg))

    modules = []

    # -m *
    if input_module == '*':
        for parent, dirnames, filenames in os.walk(paths.SCRIPT_PATH, followlinks=True):
            if len(filenames) == 0:
                msg = 'Module [%s] is null.' % paths.SCRIPT_PATH
                logger.error(msg)

            for each in filenames:
                if '__init__' in each:
                    continue
                file_path = os.path.join(parent, each)
                modules.append('.'.join(re.split('[\\\\/]',file_path[_len:-3])))
    else:
        # -m test,./script/test.py,@www
        for _module in input_module.split(','):

            # @www
            if _module.startswith("@"):
                module_name_list = glob.glob(os.path.join(paths.SCRIPT_PATH,_module[1:], '*.py'))

                if len(module_name_list) == 0:
                    msg = 'Module [%s] is not exist.' % _module
                    logger.error(msg)
                else:
                    for each in module_name_list:
                        if '__init__' in each:
                            continue
                        modules.append('.'.join(re.split('[\\\\/]',each[_len:-3])))

            else:
                if not _module.endswith('.py'):
                    _module += '.py'

                # handle input: "-m ./script/test.py"
                if  os.path.split(_module)[0]:
                    _path = os.path.abspath(os.path.join(paths.ROOT_PATH, _module))

                # handle input: "-m test"  "-m test.py"
                else:
                    _path = os.path.abspath(os.path.join(paths.SCRIPT_PATH, _module))
                if os.path.isfile(_path):
                    modules.append('.'.join(re.split('[\\\\/]', _path[_len:-3])))
                else:
                    msg = 'Module is\'t exist: %s' % _module
                    logger.error(_path)
                    logger.error(msg)

    conf['modules_name'] = list(set(modules))
    logger.debug("Set module: %s." % input_module)


def target_register(args):

    if args.target_simple:
        conf['target_simple'] = args.target_simple
        logger.debug("Set target: %s." % conf['target_simple'])

    elif args.target_file:
        if os.path.isfile(args.target_file):
            conf['target_file'] = args.target_file
        else:
            msg = 'Target file not exist: %s' % args.target_file
            sys.exit(logger.error(msg))
        logger.debug("Set target: %s." % conf['target_file'])

    elif args.target_nmap_xml:
        if os.path.isfile(args.target_nmap_xml):
            conf['target_nmap_xml'] = args.target_nmap_xml
        else:
            msg = 'Target file not exist: %s' % args.target_nmap_xml
            sys.exit(logger.error(msg))
        logger.debug("Set target: %s." % conf['target_nmap_xml'])

    elif args.target_network:
        conf['target_network'] = args.target_network
        logger.debug("Set target: %s." % conf['target_network'])

    elif args.target_task:
        conf['target_task'] = args.target_task
        logger.debug("Set target: %s." % conf['target_task'])

    elif args.target_search_engine:
        conf['target_search_engine'] = args.target_search_engine
        logger.debug("Set target: %s." % conf['target_search_engine'])

    elif args.target_zoomeye:
        conf['target_zoomeye'] = args.target_zoomeye
        logger.debug("Set target: %s." % conf['target_zoomeye'])

    elif args.target_shodan:
        conf['target_shodan'] = args.target_shodan
        logger.debug("Set target: %s." % conf['target_shodan'])

    elif args.target_fofa:
        conf['target_fofa'] = args.target_fofa
        logger.debug("Set target: %s." % conf['target_fofa'])

    elif args.target_fofa_today_poc:
        conf['target_fofa_today_poc'] = args.target_fofa_today_poc
        logger.debug("Set target: %s." % conf['target_fofa_today_poc'])

    elif args.target_google:
        conf['target_google'] = args.target_google
        logger.debug("Set target: %s." % conf['target_google'])

    elif args.target_github:
        conf['target_github'] = args.target_github
        logger.debug("Set target: %s." % conf['target_github'])

    else:
        exit(logger.error("Can't find any targets. Please load target by -iS/iN/iF/iX/iE/iT/gg/ff/fft/ze/sd/gh."))

    if args.target_port:
        if args.target_port >0 and args.target_port < 65536:
            conf['target_port'] = args.target_port
            logger.debug("Set port: %s." % conf['target_port'])
        else:
            msg = 'Invalid input port: %s.' % args.target_port
            sys.exit(logger.error(msg))


def show_task(args):

    if args.task_show:

        if os.path.isfile(paths.DATABASE_PATH):
            datadase = Database(paths.DATABASE_PATH)
            datadase.connect()
            rows = datadase.select_taskid(args.task_show)

            for row in rows:
                msg = "Taskid: %s, Status: %s, Value: %s" %(row[1], row[2], unserialize_object(row[3]))
                logger.sysinfo(msg)

            if len(rows) == 0:
                logger.error("The %s session is not exist! So we show all sessions as follow:  " %(args.task_show))
                rows = datadase.select_all()
                for row in rows:
                    msg = "Taskid: %s, Status: %s, Value: %s" % (row[1], row[2], unserialize_object(row[3]))
                    logger.sysinfo(msg)
            else:
                datas = []
                file = os.path.join(paths.DATA_PATH, args.task_show)

                if os.path.isfile(file):
                    hashdb = HashDB(file)
                    hashdb.connect()
                    for _row in hashdb.select_all():
                        data = {
                            "id": _row[0],
                            "tid": _row[1],
                            "flag": _row[2],
                            'target_host': _row[3],
                            'target_port': _row[4],
                            'url': _row[5],
                            'module_name': _row[6],
                            "data": unserialize_object(_row[7]),
                            "res": unserialize_object(_row[8]),
                            "other": unserialize_object(_row[9])
                        }

                        if conf.OUT != None:
                            datas.append(data)
                        else:
                            print_dic(data)

                    if conf.OUT != None :
                        output_excal(datas,conf.OUT.task_show)
                else:
                    logger.error("The %s session_file is not exist. " % (args.task_show))
        else:
            logger.error("The storage_file is not exist. ")

        sys.exit()