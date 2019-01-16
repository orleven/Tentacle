#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.utils import random_MD5
from lib.core.options import init_options
from lib.core.engine import Engine
from lib.core.data import paths
from lib.core.data import logger
from lib.core.data import engine
from lib.core.database import Database
from lib.core.settings import TASK_INIT_STATUS
from lib.core.settings import TASK_RUN_STATUS
from lib.core.settings import TASK_COMPLETE_STATUS
from lib.core.common import get_time

def normal(args):

    name = random_MD5()[8:-8]
    init_options(args)

    database = Database(paths.DATABASE_PATH)
    database.connect()
    database.init()
    database.insert_task(name, args, TASK_INIT_STATUS,get_time())

    engine = Engine(name)
    engine.load_modules()
    engine.load_function()
    engine.load_targets()
    engine.load_parameter()

    database.update_task_status(name, TASK_RUN_STATUS,get_time())
    engine.run()
    database.update_task_status(name, TASK_COMPLETE_STATUS,get_time())
