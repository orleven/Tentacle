#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import os
import time
import socket
import tempfile
import contextlib


from lib.api.api import myserver

from lib.api.api import myclient

from lib.utils.utils import  random_MD5
from lib.utils.convert import byte2hex
from lib.core.options import init_options
from lib.core.engine import Engine
from lib.core.module import load_module,load_target

from lib.core.data import paths
from lib.core.data import logger

from lib.core.data import conf
from lib.core.database import Database
from lib.core.enums import MKSTEMP_PREFIX
from lib.core.common import get_safe_ex_string
from lib.core.settings import RESTAPI_DEFAULT_HOST
from lib.core.settings import RESTAPI_DEFAULT_PORT
from lib.core.settings import RESTAPI_DEFAULT_ADAPTER
from lib.core.settings import TASK_INIT_STATUS
from lib.core.settings import TASK_RUN_STATUS
from lib.core.settings import TASK_COMPLETE_STATUS
from thirdparty.bottle.bottle import server_names
from thirdparty.bottle.bottle import run



def normal(args):
    name = random_MD5()[8:-8]
    # configFileParser(os.path.join(paths.w9scan_ROOT_PATH, "config.conf"))
    init_options(args)
    database = Database(os.path.join(paths.DATA_PATH, 'storage'))
    database.connect()
    database.init()
    database.insert_task(name, args, TASK_INIT_STATUS)

    engine = Engine(name)
    engine.load_modules()
    engine.load_targets()
    database.update_task_status(name, TASK_RUN_STATUS)
    engine.run()
    database.update_task_status(name, TASK_COMPLETE_STATUS)



def server(host=RESTAPI_DEFAULT_HOST, port=RESTAPI_DEFAULT_PORT, adapter=RESTAPI_DEFAULT_ADAPTER, username=None, password=None):
    myserver(host, port, adapter, username, password)

def client(host=RESTAPI_DEFAULT_HOST, port=RESTAPI_DEFAULT_PORT, username=None, password=None):
    myclient(host, port, username, password)

