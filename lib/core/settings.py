#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import random
import re
import types
import sys

AGENTS_LIST = [
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
]

HEADERS = {
    'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'User-Agent': random.choice(AGENTS_LIST),
}

'''
    curl -X POST https://api.zoomeye.org/user/login -d '
    {
    "username": "username@qq.com",
    "password": "password"
    }'
'''


GIT_REPOSITORY = "https://github.com/orleven/tentacle.git"

# String representation for NULL value
NULL = "NULL"

# Encoding used for Unicode data
UNICODE_ENCODING = "utf-8"

# Default REST-JSON API server listen port
RESTAPI_DEFAULT_PORT = 8775

RESTAPI_DEFAULT_HOST = "127.0.0.1"

# Default adapter to use for bottle server
RESTAPI_DEFAULT_ADAPTER = "wsgiref"

# System variables
IS_WIN = True if sys.platform == 'win32' else False

VERSION = "0.1.1"
SITE = "http://www.orleven.com"
TYPE_COLORS = {"dev": 33, "test": 90, "pip": 34}
TYPE = "dev" if VERSION.count('.') > 2 and VERSION.split('.')[-1] != '0' else "test"
VERSION_STRING = "tentacle/%s#%s" % ('.'.join(VERSION.split('.')[:-1]) if VERSION.count('.') > 2 and VERSION.split('.')[-1] == '0' else VERSION, TYPE)

# colorful banner
BANNER = """\033[01;33m\
.___________. _______ .__   __. .___________.    ___       ______  __       _______
|           ||   ____||  \ |  | |           |   /   \     /      ||  |     |   ____|\033[01;37m{\033[01;%dm%s\033[01;37m}\033[01;33m
`---|  |----`|  |__   |   \|  | `---|  |----`  /  ^  \   |  ,----'|  |     |  |__
    |  |     |   __|  |  . `  |     |  |      /  /_\  \  |  |     |  |     |   __|
    |  |     |  |____ |  |\   |     |  |     /  _____  \ |  `----.|  `----.|  |____
    |__|     |_______||__| \__|     |__|    /__/     \__\ \______||_______||_______| \033[0m\033[4;37m%s\033[0m\n

""" % (TYPE_COLORS.get(TYPE, 31), VERSION_STRING.split('/')[-1], SITE)

# Alphabet used for heuristic checks
HEURISTIC_CHECK_ALPHABET = ('"', '\'', ')', '(', ',', '.')

# Minor artistic touch
BANNER = re.sub(r"\[.\]", lambda _: "[\033[01;41m%s\033[01;49m]" % random.sample(HEURISTIC_CHECK_ALPHABET, 1)[0], BANNER)

# PICKLE_REDUCE_WHITELIST = (types.Number, types.DictType, types.FloatType, types.IntType, types.ListType, types.LongType, types.NoneType, types.StringType, types.TupleType, types.UnicodeType, types.XRangeType, type(AttribDict()), type(set()))


# Skip unforced HashDB flush requests below the threshold number of cached items
HASHDB_FLUSH_THRESHOLD = 32

# Number of retries for unsuccessful HashDB flush attempts
HASHDB_FLUSH_RETRIES = 3

# Number of retries for unsuccessful HashDB retrieve attempts
HASHDB_RETRIEVE_RETRIES = 3

# Number of retries for unsuccessful HashDB end transaction attempts
HASHDB_END_TRANSACTION_RETRIES = 3


TASK_INIT_STATUS = 0
TASK_RUN_STATUS = 1
TASK_STOP_STATUS = -1
TASK_COMPLETE_STATUS = 2
