#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import os
import sys

# 不生成pyc
sys.dont_write_bytecode = True

# 最低python运行版本
REQUIRE_PY_VERSION = (3, 9)

# 检测当前运行版本
RUN_PY_VERSION = sys.version_info
if RUN_PY_VERSION < REQUIRE_PY_VERSION:
    exit(f"[-] Incompatible Python version detected ('{RUN_PY_VERSION}). For successfully running program you'll have to use version {REQUIRE_PY_VERSION}  (visit 'http://www.python.org/download/')")

# 项目名称
PROJECT_NAME = "Tentacle"

# 当前扫描器版本
VERSION = "1.0"

# 版本描述
VERSION_STRING = f"{PROJECT_NAME}/{VERSION}"

# GIT
GIT_REPOSITORY = "https://github.com/orleven/tentacle.git"

# 描述
DESCRIPTION = 'Tentacle is a POC vulnerability verification and exploit framework based on Sqlmap and POC-T. It supports free extension of exploits and uses POC scripts. It supports calls to zoomeye, fofa, shodan and other APIs to perform bulk vulnerability verification for multiple targets.'

# Site
SITE = "http://www.orleven.com/"

# Banner
BANNER = """\033[01;33m\
.___________. _______ .__   __. .___________.    ___       ______  __       _______
|           ||   ____||  \ |  | |           |   /   \     /      ||  |     |   ____| \033[01;37m{\033[01;%dm%s\033[01;37m}\033[01;33m
`---|  |----`|  |__   |   \|  | `---|  |----`  /  ^  \   |  ,----'|  |     |  |__
    |  |     |   __|  |  . `  |     |  |      /  /_\  \  |  |     |  |     |   __|
    |  |     |  |____ |  |\   |     |  |     /  _____  \ |  `----.|  `----.|  |____
    |__|     |_______||__| \__|     |__|    /__/     \__\ \______||_______||_______| \033[0m\033[4;37m%s\033[0m\n

""" % (90, VERSION_STRING, SITE)

# 当前运行入口文件
MAIN_NAME = os.path.split(os.path.splitext(sys.argv[0])[0])[-1]

# 当前运行路径
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 工具路径
TOOL = 'tool'
TOOL_PATH = os.path.join(ROOT_PATH, TOOL)

# 日志路径
LOG = 'log'
LOG_PATH = os.path.join(ROOT_PATH, LOG)

# 配置路径
CONFIG = 'conf'
CONFIG_PATH = os.path.join(ROOT_PATH, CONFIG)

# 配置文件路径
CONFIG_FILE = f"{PROJECT_NAME}.conf"
CONFIG_FILE_PATH = os.path.join(CONFIG_PATH, CONFIG_FILE)

# 相关Addon路径
SCRIPT = 'script'
SCRIPT_PATH = os.path.join(ROOT_PATH, SCRIPT)

VUL = 'vul'
VUL_SCRIPT_PATH = os.path.join(SCRIPT_PATH, VUL)

PORT = 'port'
PORT_SCRIPT_PATH = os.path.join(SCRIPT_PATH, PORT)

SPECIAL = 'special'
SPECIAL_SCRIPT_PATH = os.path.join(SCRIPT_PATH, SPECIAL)

INFO = 'info'
INFO_SCRIPT_PATH = os.path.join(SCRIPT_PATH, INFO)

TEST = 'test'
TEST_SCRIPT_PATH = os.path.join(SCRIPT_PATH, TEST)

# 相关Data路径
DATA = 'data'
DATA_PATH = os.path.join(ROOT_PATH, DATA)

# 相关输出路径
OUTPUT = 'output'
OUTPUT_PATH = os.path.join(ROOT_PATH, OUTPUT)

# 相关输出路径
DICT = 'dict'
DICT_PATH = os.path.join(ROOT_PATH, DICT)

# INDEX_DATABASE
INDEX_DATABASE = 'index'