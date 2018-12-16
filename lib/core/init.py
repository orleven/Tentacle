#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import os
import sys
from lib.core.settings import INDEX_DATABASE
from lib.core.data import logger
from lib.core.data import paths
from lib.core.config import init_conf
from lib.core.config import load_conf
from lib.core.enums import CUSTOM_LOGGING
from lib.core.update import update_program

def initialize(args):

    if args.debug:
        logger.set_level(CUSTOM_LOGGING.DEBUG)
    set_paths()
    check_update(args)
    config_parser()

def check_update(args):
    if args.update:
        update_program()
        sys.exit(0)

def set_paths():
    try:
        os.path.isdir(paths.ROOT_PATH)
    except UnicodeEncodeError:
        errMsg = "Your system does not properly handle non-ASCII paths. "
        errMsg += "Please move the project root directory to another location"
        exit(errMsg)
        raise SystemExit

    logger.debug("Initialize tentacle path...")
    paths.LOG_PATH = os.path.join(paths.ROOT_PATH, "log")
    paths.OUTPUT_PATH = os.path.join(paths.ROOT_PATH, "output")
    paths.SCRIPT_PATH = os.path.join(paths.ROOT_PATH, "script")
    paths.DICT_PATH = os.path.join(paths.ROOT_PATH, "dict")
    paths.CONFIG_PATH = os.path.join(paths.ROOT_PATH, "conf")
    paths.DATA_PATH = os.path.join(paths.ROOT_PATH, "data")
    paths.TOOL_PATH = os.path.join(paths.ROOT_PATH, "tool")

    for path in paths.values():
        if not any(path.endswith(_) for _ in (".txt", ".xml", ".zip")):
            if not os.path.exists(path):
                os.mkdir(path)

    paths.DATABASE_PATH = os.path.join(paths.DATA_PATH, INDEX_DATABASE)

def config_parser():
    path = os.path.join(paths.CONFIG_PATH, "tentacle.conf")
    if not os.path.exists(path):
        init_conf(path)
    load_conf(path)


