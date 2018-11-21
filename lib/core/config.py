#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'


import os
import sys
from lib.core.data import logger
from lib.core.data import conf
import configparser




def init_conf(path):
    logger.debug("Init tentacle config...")
    configs = {
        "basic": {
            # "timeout": "5",

        },
        "proxy": {
            "http_proxy": "http://127.0.0.1:1080",
            "https_proxy": "https://127.0.0.1:1080"
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
    }
    cf = configparser.ConfigParser()
    for section in configs.keys():
        cf[section] = configs[section]
    with open(path, 'w+') as configfile:
        cf.write(configfile)
    sys.exit(logger.error("Please set the tentacle config in tentacle.conf..."))

def load_conf(path):
    logger.debug("Load tentacle config...")
    cf = configparser.ConfigParser()
    cf.read(path)
    sections = cf.sections()
    configs = {}
    for section in sections:
        logger.debug("Load config: %s" % (section))
        config = {}
        for option in cf.options(section):
            config[option] = cf.get(section,option)
        configs[section] = config
    conf['config'] = configs

def update_conf(path,section,option,value):
    logger.debug("Update tentacle config: [%s][%s] => %s" %(section,option,value))
    cf = configparser.ConfigParser()
    cf.set(section,option,value)
    with open(path, 'w+') as configfile:
        cf.write(configfile)
