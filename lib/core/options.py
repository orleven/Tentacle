#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import os
import sys
from lib.utils.output import print_dic
from lib.core.common import unserialize_object
from lib.core.database import TaskDataDB
from lib.core.database import TaskDB
from lib.core.data import logger
from lib.core.data import conf
from lib.core.data import paths
from lib.utils.output import output_excal

def init_options(args):

    conf.VERBOSE = args.verbose
    conf.OUT = args.out

    show_task(args)

    if  not 0 < args.thread < 501:
        msg = 'Invalid input in [-t] for thread num, range: 1 to 500.'
        sys.exit(logger.error(msg))

    conf['skip_port_scan'] = args.skip_port_scan
    conf['thread_num'] = args.thread
    logger.sysinfo("Set timeout: %s" % (conf['basic']['timeout']))
    logger.sysinfo("Set thread: %s" % str(conf['thread_num']))

def show_task(args):

    if args.task_show:

        if os.path.isfile(paths.DATABASE_PATH):
            datadase = TaskDB(paths.DATABASE_PATH)
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
                    hashdb = TaskDataDB(file)
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
                            "req": unserialize_object(_row[7]),
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
