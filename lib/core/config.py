#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.core.data import logger
from lib.core.data import conf
import configparser

def load_conf(path):
    logger.debug("Load tentacle config...")
    cf = configparser.ConfigParser()
    cf.read(path)
    sections = cf.sections()
    for section in sections:
        logger.debug("Load config: %s" % (section))
        config = {}
        for option in cf.options(section):
            config[option] = cf.get(section,option)
        conf[section] = config


def update_conf(path,section,option,value):
    logger.debug("Update tentacle config: [%s][%s] => %s" %(section,option,value))
    cf = configparser.ConfigParser()
    cf.set(section,option,value)
    with open(path, 'w+') as configfile:
        cf.write(configfile)

def init_conf(path):
    logger.sysinfo("Init tentacle config...")
    configs = {
        "basic": {
            "timeout": "5",
            "max_retries": "0",
        },
        "proxy": {
            "proxy": False,
            "proxy_url": "socks5://127.0.0.1:1080",
        },
        "google_api": {
            "developer_key": "developer_key",
            "search_enging": "developer_key"
        },
        "zoomeye_api": {
            "username": "token@orleven.com",
            "password": "tentacle_123456"
        },
        "fofa_api": {
            "email": "test@orleven.com",
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

