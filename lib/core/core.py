#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.core.common import random_MD5
from lib.core.options import init_options
from lib.core.data import paths
from lib.core.database import TaskDB
from lib.core.engine import Engine
from lib.core.enums import TASK_STATUS
from lib.core.common import get_time

def normal(args):

    name = random_MD5()[8:-8]
    init_options(args)

    database = TaskDB(paths.DATABASE_PATH)
    database.connect()
    database.init()
    database.insert_task(name, args, TASK_STATUS.TASK_INIT_STATUS,get_time())

    engine = Engine(name)
    engine.load_config()
    engine.load_modules()
    engine.load_function()
    engine.load_parameter()
    engine.load_targets()

    database.update_task_status(name, TASK_STATUS.TASK_RUN_STATUS,get_time())
    engine.run()
    database.update_task_status(name, TASK_STATUS.TASK_COMPLETE_STATUS,get_time())
