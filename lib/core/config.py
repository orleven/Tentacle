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
    configs = {}
    for section in sections:
        logger.debug("Load config: %s" % (section))
        config = {}
        for option in cf.options(section):
            config[option] = cf.get(section,option)
        configs[section] = config
    conf['config'] = configs
    # conf['config']['basic']['user_agent'] = conf['config']['basic']['user_agent'].split('\n')

def update_conf(path,section,option,value):
    logger.debug("Update tentacle config: [%s][%s] => %s" %(section,option,value))
    cf = configparser.ConfigParser()
    cf.set(section,option,value)
    with open(path, 'w+') as configfile:
        cf.write(configfile)

