#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import os
import sys
from lib.core.data import paths


def set_paths(rootPath):
    """
    Sets absolute paths for project directories and files
    """
    paths.ROOT_PATH = rootPath

    try:
        os.path.isdir(paths.ROOT_PATH)
    except UnicodeEncodeError:
        errMsg = "your system does not properly handle non-ASCII paths. "
        errMsg += "Please move the project root directory to another location"
        exit(errMsg)
        raise SystemExit


    # tentacle paths
    paths.LOG_PATH = os.path.join(paths.ROOT_PATH, "log")
    paths.OUTPUT_PATH = os.path.join(paths.ROOT_PATH, "output")
    paths.SCRIPT_PATH = os.path.join(paths.ROOT_PATH, "script")
    paths.DICT_PATH = os.path.join(paths.ROOT_PATH, "dict")
    paths.CONFIG_PATH = os.path.join(paths.ROOT_PATH, "conf")
    paths.DATA_PATH = os.path.join(paths.ROOT_PATH, "data")
    paths.TOOL_PATH = os.path.join(paths.ROOT_PATH, "tool")

    # telntacle files
    # paths.COMMON_PASS_DICY = os.path.join(paths.DICT_PATH, "passwords.txt")
    # paths.COMMON_USER_DICY = os.path.join(paths.DICT_PATH, "usernames.txt")
    # paths.USER_AGENT_DICY = os.path.join(paths.DICT_PATH, "user-agent.txt")

    for path in paths.values():
        if not any(path.endswith(_) for _ in (".txt", ".xml", ".zip")):
            if not os.path.exists(path):
                os.mkdir(path)
        # else:
            # checkFile(path)
