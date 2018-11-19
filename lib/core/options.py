#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import re
import sys
import glob
import time
import os
from lib.utils.output import print_dic
from lib.core.common import unserialize_object
from lib.core.hashdb import HashDB
from lib.core.database import Database
from lib.core.data import logger
from lib.core.data import conf
from lib.core.data import paths
from lib.core.enums import CUSTOM_LOGGING
from lib.core.enums import  ENGINE_MODE_STATUS
from lib.utils.output import to_excal
from lib.core.update import update_program

def init_options(args):
    # if args.module == ''
    # conf.MODULE_NAME =
    # -------------------------------
    # 以下内容不用修改 20181114

    conf.VERBOSE = args.verbose
    conf.OUT = args.out


    check_update(args)
    show_task(args)
    module_register(args)
    function_register(args)
    engine_register(args)
    target_register(args)
    # dict_register(args, name)
    # ---------------------------

    # 此模块有待改进
    # task_register(args, name)
    # module_register(args, name)
    # return name



def check_update(args):
    if args.update:
        update_program()
        sys.exit(0)


def function_register(args):
    if args.function:
        conf['func_name'] = args.function
        # conf.FUNCTION = args.function # 以后删
    else:
        conf['func_name'] = 'prove'





# def dict_register(args,name):
#
#     if args.dic_one:
#         if os.path.isfile(args.dic_one):
#             engine[name]['dic_one'] = args.dic_one
#             # msg = "Load dic1(%s): %s" % (args.dic_one)
#             # logger.info("Load dic1("+name+"): "+ args.dic_one)
#         else:
#             logger.error("Error dic1("+name+"): "+ args.dic_one + " is not file.")
#
#     if args.dic_two:
#         if os.path.isfile(args.dic_two):
#             engine[name]['dic_two'] = args.dic_two
#             logger.info("Load dic2(" + name + "): " + args.dic_two)
#         else:
#             logger.error("Error dic2(" + name + "): " + args.dic_two + " is not file.")
#
#
#     # if args.dic_mode <0 or args.dic_mode > 2:
#     #     msg = 'Burst mode Error. Use [-dM 1] or [-dM 2] to set burst mode.'
#     #     sys.exit(logger.info(msg))
#     # else:
#     #     engine[name]['dic_mode'] = args.dic_mode

def engine_register(args):

    # if args.engine_gevent ^ args.engine_gevent:
    #     if args.engine_gevent:
    #         conf['engine_type'] = ENGINE_MODE_STATUS.GEVENT
    #     else:
    #         conf['engine_type'] = ENGINE_MODE_STATUS.GEVENT
    # else:
    #     if args.engine_gevent:
    #         msg = "Error for engine's type, can't choice dubble types."
    #         msg += 'Use [-eT] to set Multi-Threaded mode or [-eG] to set Gevent mode.'
    #         sys.exit(logger.error(msg))
    #     else:
    #         msg ='Default choice Multi-Threaded mode.'
    #         logger.sysinfo(msg)
    #         conf['engine_type'] =  ENGINE_MODE_STATUS.THREAD  # default choice


    if  not 0 < args.thread < 501:
        msg = 'Invalid input in [-t], range: 1 to 500'
        sys.exit(logger.error(msg))

    conf['thread_num'] = args.thread

def module_register(args):
    _len = len(paths.ROOT_PATH) + 1
    if args.show:
        msg = 'There are available modules as follows: \r\n'
        for parent, dirnames, filenames in os.walk(paths.SCRIPT_PATH, followlinks=True):
            for each in filenames:
                if '__init__' in each:
                    continue
                file_path = os.path.join(parent, each)
                msg += 'Script modual: %s\r\n'% file_path[_len:-3]
        sys.exit(logger.sysinfo(msg))
        # module_name_list = glob.glob(os.path.join(paths.SCRIPT_PATH, '*.py'))
        # msg = 'Script modual(total:%s)\n' % str(len(module_name_list) - 1)
        # for each in module_name_list:
        #     _str = os.path.splitext(os.path.split(each)[1])[0]
        #     if _str not in ['__init__']:
        #         msg += 'Script modual: %s\n'% _str
        # sys.exit(logger.sysinfo(msg))


    input_module = args.module
    if not input_module:
        msg = 'Use -m to load module. Example: [-m test] or [-m ./script/test.py]'
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

        if len(modules) < 0:
            msg = 'Can\'t find any modules. Please check you input.' % _module
            sys.exit(logger.error(msg))

    conf['modules_name'] = list(set(modules))



def target_register(args):

    if args.target_simple:
        conf['target_simple'] = args.target_simple

    elif args.target_file:
        if os.path.isfile(args.target_file):
            conf['target_file'] = args.target_file
        else:
            msg = 'Target file not exist: %s' % args.target_file
            sys.exit(logger.error(msg))

    elif args.target_network:
        conf['target_network'] = args.target_network

    elif args.target_task:
        conf['target_task'] = args.target_task

    elif args.target_search_engine:
        conf['target_search_engine'] = args.target_search_engine

    elif args.target_zoomeye:
        conf['target_zoomeye'] = args.target_zoomeye

    else:
        exit(logger.error("Can't find any targets. Please load target by iS/iN/iF."))


    if args.target_port:
        if args.target_port >0 and args.target_port < 65536:
            conf['target_port'] = args.target_port
        else:
            msg = 'Invalid port : %s' % args.target_port
            sys.exit(logger.error(msg))
    # else:
    #     msg = 'Target not exist. Example: [-iL /etc/target.txt] or [-iS localhost] or [iN 192.168.111.0/24]'
    #     sys.exit(logger.error(msg))

def show_task(args):
    if args.task_show:
        conf.ENGINE = ENGINE_MODE_STATUS.THREAD  # default choice
        file = os.path.join(paths.DATA_PATH, 'storage')
        if os.path.isfile(file):
            datadase = Database(os.path.join(paths.DATA_PATH, 'storage'))
            datadase.connect()
            rows =  datadase.select(args.task_show)
            # print(rows)
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
                    hashdb = HashDB(os.path.join(paths.DATA_PATH, args.task_show))
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
                        to_excal(datas,conf.OUT.task_show)
                else:
                    logger.error("The %s session_file is not exist. " % (args.task_show))
        else:
            logger.error("The storage_file is not exist. ")
        sys.exit()