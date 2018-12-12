#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import hashlib
import random
import time
from string import ascii_lowercase
from string import digits
from lib.utils.cipher import md5

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