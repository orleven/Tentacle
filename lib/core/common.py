#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import time
import random
from lib.utils.cipher import base64pickle
from lib.utils.cipher import base64unpickle
from lib.utils.output import data_to_stdout

def serialize_object(object_):
    return base64pickle(object_)

def unserialize_object(value):
    return base64unpickle(value) if value else None

def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_timestamp():
    return int(round(time.time() * 1000))

def random_IP():
    return '.'.join([str(random.randint(0, 255)) for x in range(0,4)])

def get_safe_ex_string(ex, encoding=None):
    """
    Safe way how to get the proper exception represtation as a string
    (Note: errors to be avoided: 1) "%s" % Exception(u'\u0161') and 2) "%s" % str(Exception(u'\u0161'))

    >>> get_safe_ex_string(Exception('foobar'))
    u'foobar'
    """

    retVal = ex

    if getattr(ex, "message", None):
        retVal = ex.message
    elif getattr(ex, "msg", None):
        retVal = ex.msg
    return retVal.strip()
    # return getUnicode(retVal or "", encoding=encoding).strip()

def poll_process(process, suppress_errors=False):
    """
    Checks for process status (prints . if still running)
    """

    while True:
        data_to_stdout(".")
        time.sleep(1)

        returncode = process.poll()

        if returncode is not None:
            if not suppress_errors:
                if returncode == 0:
                    data_to_stdout(" done\n")
                elif returncode < 0:
                    data_to_stdout(" process terminated by signal %d\n" % returncode)
                elif returncode > 0:
                    data_to_stdout(" quit unexpectedly with return code %d\n" % returncode)

            break
