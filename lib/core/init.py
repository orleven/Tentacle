#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import os
import sys
import configparser
from lib.core.settings import INDEX_DATABASE
from lib.core.data import logger
from lib.core.data import paths
from lib.core.config import load_conf
from lib.core.enums import CUSTOM_LOGGING
from lib.core.update import update_program
from lib.core.settings import DATA_PATH
from lib.core.settings import OUTPUT_PATH
from lib.core.settings import SCRIPT_PATH
from lib.core.settings import SPECIAL_SCRIPT_PATH
from lib.core.settings import DICT_PATH
from lib.core.settings import CONFIG_PATH
from lib.core.settings import LOG_PATH
from lib.core.settings import CONFIG_FILE

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
    paths.LOG_PATH = os.path.join(paths.ROOT_PATH, LOG_PATH)
    paths.OUTPUT_PATH = os.path.join(paths.ROOT_PATH, OUTPUT_PATH)
    paths.SCRIPT_PATH = os.path.join(paths.ROOT_PATH, SCRIPT_PATH)
    paths.SPECIAL_SCRIPT_PATH = os.path.join(paths.ROOT_PATH,SPECIAL_SCRIPT_PATH)
    paths.DICT_PATH = os.path.join(paths.ROOT_PATH, DICT_PATH)
    paths.CONFIG_PATH = os.path.join(paths.ROOT_PATH,CONFIG_PATH)
    paths.DATA_PATH = os.path.join(paths.ROOT_PATH,DATA_PATH)

    for path in paths.values():
        if not any(path.endswith(_) for _ in (".txt", ".xml", ".zip")):
            if not os.path.exists(path):
                os.mkdir(path)

    paths.DATABASE_PATH = os.path.join(paths.DATA_PATH, INDEX_DATABASE)

def config_parser():
    path = os.path.join(paths.CONFIG_PATH, CONFIG_FILE)
    if not os.path.exists(path):
        init_conf(path)
    load_conf(path)


def init_conf(path):
    logger.debug("Init tentacle config...")
    configs = {
        "basic": {
            "timeout": "5",
            "max_retries": "0",
        },
        "proxy": {
            "proxy": False,
            "socks5": "127.0.0.1:1080",
            # "http_proxy": "http://127.0.0.1:1080",
            # "https_proxy": "https://127.0.0.1:1080"
        },
        "google_api": {
            "developer_key": "developer_key",
            "search_enging": "developer_key"
        },
        "zoomeye_api": {
            "username": "token@orlven.com",
            "password": "tentacle_123456"
        },
        "fofa_api": {
            "email": "test@orlven.com",
            "token": "tentacle_123456"
        },
        "shodan_api": {
            "token": "token@tentacle"
        },
        "github_api": {
            "token": "token@tentacle",
        },
        "ceye_api":{
            "identifier": "test.ceye.io",
            "token": "66ca15b9e782b5127d846af76bbe2aa1"
        }
    }
    cf = configparser.ConfigParser()
    for section in configs.keys():
        cf[section] = configs[section]
    with open(path, 'w+') as configfile:
        cf.write(configfile)
    sys.exit(logger.error("Please set the tentacle config in %s..." % CONFIG_FILE))
