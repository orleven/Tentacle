#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import hashlib
import pickle
from base64 import b64encode
from base64 import b64decode
from urllib.parse import unquote
from urllib.parse import quote

def md5(message):
    """md5"""
    obj = hashlib.md5()
    obj.update(message.encode(encoding='utf-8'))
    return obj.hexdigest()


def get_file_md5(file_path):
    """获取文件md5"""
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
    return str(_hash).upper()



def urldecode(value, encoding='utf-8'):
    """url解码"""

    return unquote(value, encoding)


def safe_urldecode(value, encoding='utf-8'):
    """url解码, 不报错版"""

    try:
        return urldecode(value, encoding)
    except:
        return None


def urlencode(value, encoding='utf-8'):
    """url编码"""

    return quote(value, encoding)

def safe_urlencode(value, encoding='utf-8'):
    """url编码, 不报错版"""
    try:
        return urlencode(value, encoding)
    except:
        return None


def base64encode(value, table=None, encoding='utf-8'):
    """base64编码"""
    b64_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    if type(value) is not bytes:
        value = bytes(value, encoding)
    if table:
        return str(str.translate(str(b64encode(value)), str.maketrans(b64_table, table)))[2:-1]
    else:
        return str(b64encode(value), encoding=encoding)


def safe_base64encode(value, table=None, encoding='utf-8'):
    """base64编码, 不报错版"""
    try:
        return base64encode(value, table, encoding)
    except:
        return None


def base64decode(value, table=None, encoding='utf-8'):
    """base64解码"""
    b64_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    if table:
        return b64decode(str.translate(value, str.maketrans(table, b64_table)))
    else:
        if type(value) is not bytes:
            value = bytes(value, encoding)
        return b64decode(value)


def safe_base64decode(value, table=None, encoding='utf-8'):
    """base64解码, 不报错版"""
    try:
        result = base64decode(value, table, encoding)
        if isinstance(result, bytes):
            result = result.decode(encoding)
        return result
    except:
        return None


def base64pickle(value):
    retVal = None
    try:
        retVal = safe_base64encode(pickle.dumps(value, pickle.HIGHEST_PROTOCOL))
    except:
        warnMsg = "problem occurred while serializing "
        warnMsg += "instance of a type '%s'" % type(value)
        try:
            retVal = safe_base64encode(pickle.dumps(value))
        except:
            retVal = safe_base64encode(pickle.dumps(str(value), pickle.HIGHEST_PROTOCOL))
    return retVal

def base64unpickle(value, unsafe=False):

    def loads(str):
        return pickle.loads(str)

    try:
        retVal = loads(b64decode(value))
    except TypeError:
        retVal = loads(b64decode(bytes(value)))

    return retVal