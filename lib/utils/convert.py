#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import re
import json
from functools import reduce

base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]


def bin2dec(string_num):
    return str(int(string_num, 2))

def bin2hex(string_num):
    return dec2hex(bin2dec(string_num))

def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])

def dec2hex(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 16)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])


def hex2bin(string_num):
    return dec2bin(hex2dec(string_num.upper()))

def hex2dec(string_num):
    return str(int(string_num.upper(), 16))

def jsonize(data):
    return json.dumps(data, sort_keys=False, indent=4)

def dejsonize(data):
    return json.loads(data)


def htmlunescape(value):
    retVal = value
    if value and isinstance(value, str):
        codes = (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&nbsp;', ' '), ('&amp;', '&'))
        retVal = reduce(lambda x, y: x.replace(y[0], y[1]), codes, retVal)
        try:
            retVal = re.sub(r"&#x([^ ;]+);", lambda match: chr(int(match.group(1), 16)), retVal)
        except ValueError:
            pass
    return retVal

def byte2hex(data):
    return data.hex()

def hex2byte(data):
    return bytes.fromhex(data)


# def stdoutencode(data):
#     retVal = None
#
#     try:
#         data = data or ""
#
#         # Reference: http://bugs.python.org/issue1602
#         if IS_WIN:
#             output = data.encode(sys.stdout.encoding, "replace")
#
#             if '?' in output and '?' not in data:
#                 warnMsg = "cannot properly display Unicode characters "
#                 warnMsg += "inside Windows OS command prompt "
#                 warnMsg += "(http://bugs.python.org/issue1602). All "
#                 warnMsg += "unhandled occurances will result in "
#                 warnMsg += "replacement with '?' character. Please, find "
#                 warnMsg += "proper character representation inside "
#                 warnMsg += "corresponding output files. "
#                 singleTimeWarnMessage(warnMsg)
#
#             retVal = output
#         else:
#             retVal = data.encode(sys.stdout.encoding)
#     except:
#         retVal = data.encode(UNICODE_ENCODING) if isinstance(data, str) else data
#
#     return retVal
