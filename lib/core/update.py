#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import os
import re
import sys
import subprocess
from lib.core.data import paths
from lib.core.data import logger
from lib.core.settings import GIT_REPOSITORY
from lib.core.common import poll_process
from lib.core.common import get_safe_ex_string

def update_program():
    success = False
    if not os.path.exists(os.path.join(paths.ROOT_PATH, ".git")):
        msg = "Have not a git repository. Please checkout the 'tentacle' repository "
        msg += "from GitHub (e.g. 'git clone --depth 1 %s tentacle')" % GIT_REPOSITORY
        logger.error(msg)
    else:
        msg = "Updating tentacle to the latest version from the gitHub repository."
        logger.sysinfo(msg)

        msg = "Tentacle will try to update itself using 'git' command."
        logger.sysinfo(msg)

        msg = "Update in progress..."
        logger.sysinfo(msg)

    try:
        process = subprocess.Popen("git checkout . && git pull %s HEAD" % GIT_REPOSITORY, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=paths.ROOT_PATH)  # Reference: http://blog.stastnarodina.com/honza-en/spot/python-unicodeencodeerror/
        poll_process(process, True)
        stdout, stderr = process.communicate()
        success = not process.returncode
    except (IOError, OSError) as ex:
        success = False
        stderr = get_safe_ex_string(ex)

    if success:
        logger.success("The latest revision '%s'" % (get_revision_number()))
    else:
        if isinstance(stderr, str):
            if "Not a git repository" in stderr:
                msg = "Not a valid git repository. Please checkout the 'orleven/tentacle' repository "
                msg += "from GitHub (e.g. 'git clone --depth 1 %s tentacle')" % GIT_REPOSITORY
                logger.error(msg)
            else:
                logger.error("Update could not be completed ('%s')" % re.sub(r"\W+", " ", stderr).strip())
        else:
            logger.error("Update could not be completed. ")

    if not success:
        if sys.platform == 'win32':
            msg = "for Windows platform it's recommended "
            msg += "to use a GitHub for Windows client for updating "
            msg += "purposes (http://windows.github.com/) or just "
            msg += "download the latest snapshot from "
            msg += GIT_REPOSITORY
        else:
            msg = "For Linux platform it's required "
            msg += "to install a standard 'git' package (e.g.: 'sudo apt-get install git')"

        logger.sysinfo(msg)


def get_revision_number():
    """
    Returns abbreviated commit hash number as retrieved with "git rev-parse --short HEAD"
    """

    retVal = None
    filePath = None
    _ = os.path.dirname(__file__)

    while True:
        filePath = os.path.join(_, ".git", "HEAD")
        if os.path.exists(filePath):
            break
        else:
            filePath = None
            if _ == os.path.dirname(_):
                break
            else:
                _ = os.path.dirname(_)

    while True:
        if filePath and os.path.isfile(filePath):
            with open(filePath, "r") as f:
                content = f.read()
                filePath = None
                if content.startswith("ref: "):
                    filePath = os.path.join(_, ".git", content.replace("ref: ", "")).strip()
                else:
                    match = re.match(r"(?i)[0-9a-f]{32}", content)
                    retVal = match.group(0) if match else None
                    break
        else:
            break

    if not retVal:
        process = subprocess.Popen("git rev-parse --verify HEAD", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        match = re.search(r"(?i)[0-9a-f]{32}", stdout or "")
        retVal = match.group(0) if match else None

    return retVal[:7] if retVal else None