#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import hashlib
import random
import time
from string import ascii_lowercase
from string import digits
from lib.utils.cipher import md5
from lib.utils.cipher import base64pickle
from lib.utils.cipher import base64unpickle
from lib.utils.output import data_to_stdout


def random_string(length=8):
    return ''.join([random.choice(ascii_lowercase) for _ in range(length)])

def random_digits(length=8):
    return ''.join([random.choice(digits) for _ in range(length)])

def random_MD5(length = 16, ret_plain = False):
    """
    生成随机MD5键值对

    :param length:指定明文长度
    :param hex:指定密文长度为32位
    :returns 原文，密文(32位或16位)
    """
    plain = random_digits(length)
    m = hashlib.md5()
    m.update(bytes(plain,'utf-8'))
    cipher = m.hexdigest() if hex else m.hexdigest()
    if ret_plain:
        return [plain, cipher]
    else:
        return cipher

def timestamp_MD5():
    return md5(str(int(round(time.time() * 1000))))

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


def poll_process(process, suppress_errors=False):
    """
    Checks for process status (prints . if still running)
    """
    while True:
        # data_to_stdout(".")
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
    else:
        retVal = str(ex)
    return retVal
    # return getUnicode(retVal or "", encoding=encoding).strip()

