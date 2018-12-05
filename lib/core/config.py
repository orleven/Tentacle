#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'


import os
import sys
import random
from lib.core.data import logger
from lib.core.data import conf
import configparser




def init_conf(path):
    logger.debug("Init tentacle config...")
    configs = {
        "basic": {
            "timeout": "5",
            "user_agent": '\n'.join([
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)',
                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; Media Center PC 3.0; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)',
                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; FDM; .NET CLR 1.1.4322)',
                'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
            ])
        },
        'rebound' :{
            'local_host': '127.0.0.1',
            'local_port': '4444',
        },
        "ssh_key":{
            "public_key" : 'ssh-rsa =====',
            "private_key" : """
-----BEGIN RSA PRIVATE KEY-----
=====
-----END RSA PRIVATE KEY-----
        """
        },
        "proxy": {
            "proxy": False,
            "socks5": "127.0.0.1:1080",
            "http_proxy": "http://127.0.0.1:1080",
            "https_proxy": "https://127.0.0.1:1080"
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

