#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import random
import re
import sys

INDEX_DATABASE = 'storage'

GIT_REPOSITORY = "https://github.com/orleven/tentacle.git"

DESCRIPTION = 'Tentacle is a POC vulnerability verification and exploit framework based on Sqlmap and POC-T. It supports free extension of exploits and uses POC scripts. It supports calls to zooeyem, fofa, shodan and other APIs to perform bulk vulnerability verification for multiple targets.'

VERSION = "1.0.0"
SITE = "http://www.orleven.com"
TYPE_COLORS = {"dev": 33, "test": 90, "pip": 34}
TYPE = "dev" if VERSION.count('.') > 2 and VERSION.split('.')[-1] != '0' else "test"
VERSION_STRING = "tentacle/%s#%s" % ('.'.join(VERSION.split('.')[:-1]) if VERSION.count('.') > 2 and VERSION.split('.')[-1] == '0' else VERSION, TYPE)
BANNER = """\033[01;33m\
.___________. _______ .__   __. .___________.    ___       ______  __       _______
|           ||   ____||  \ |  | |           |   /   \     /      ||  |     |   ____| \033[01;37m{\033[01;%dm%s\033[01;37m}\033[01;33m
`---|  |----`|  |__   |   \|  | `---|  |----`  /  ^  \   |  ,----'|  |     |  |__
    |  |     |   __|  |  . `  |     |  |      /  /_\  \  |  |     |  |     |   __|
    |  |     |  |____ |  |\   |     |  |     /  _____  \ |  `----.|  `----.|  |____
    |__|     |_______||__| \__|     |__|    /__/     \__\ \______||_______||_______| \033[0m\033[4;37m%s\033[0m\n

""" % (TYPE_COLORS.get(TYPE, 31), VERSION_STRING.split('/')[-1], SITE)
HEURISTIC_CHECK_ALPHABET = ('"', '\'', ')', '(', ',', '.')
BANNER = re.sub(r"\[.\]", lambda _: "[\033[01;41m%s\033[01;49m]" % random.sample(HEURISTIC_CHECK_ALPHABET, 1)[0], BANNER)

# System variables
IS_WIN = True if sys.platform == 'win32' else False

TASK_INIT_STATUS = 0
TASK_RUN_STATUS = 1
TASK_STOP_STATUS = -1
TASK_COMPLETE_STATUS = 2
