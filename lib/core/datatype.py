#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import copy
import types
import aiohttp
from typing import Any
class AttribDict(dict):
    """
    This class defines the object, inheriting from Python data
    type dictionary.

    >>> foo = AttribDict()
    >>> foo.bar = 1
    >>> foo.bar
    1
    """

    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}

        # Set any attributes here - before initialisation
        # these remain as normal attributes
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True

        # After initialisation, setting attributes
        # is the same as setting an item

    def __getattr__(self, item):
        """
        Maps values to attributes
        Only called if there *is NOT* an attribute with this name
        """

        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError("unable to access item '%s'" % item)

    def __setattr__(self, item, value):
        """
        Maps attributes to values
        Only if we are initialised
        """

        # This test allows attributes to be set in the __init__ method
        if "_AttribDict__initialised" not in self.__dict__:
            return dict.__setattr__(self, item, value)

        # Any normal attributes are handled normally
        elif item in self.__dict__:
            dict.__setattr__(self, item, value)

        else:
            self.__setitem__(item, value)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict

    def __deepcopy__(self, memo):
        retVal = self.__class__()
        memo[id(self)] = retVal

        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                if not isinstance(value, (types.BuiltinFunctionType, types.FunctionType, types.MethodType)):
                    setattr(retVal, attr, copy.deepcopy(value, memo))

        for key, value in self.items():
            retVal.__setitem__(key, copy.deepcopy(value, memo))

        return retVal

# class ServiceRecord():
#     def __init__(self,host, port, service, protocol, banner, fingerprint, urlrecodes):
#         self.host = host
#         self.port = port
#         self.service = service
#         self.protocol = protocol
#         self.banner = banner
#         self.fingerprint = fingerprint
#         self.urlrecodes = urlrecodes

def ensure_str(s: Any, encoding='latin1', errors='strict') -> str:
    if isinstance(s, bytes):
        return s.decode(encoding, errors)
    elif isinstance(s, str):
        return s
    else:
        return str(s)

class HTTPVersion(aiohttp.HttpVersion):
    def __str__(self):
        return f'HTTP/{self.major}.{self.minor}'

    @classmethod
    def from_aiohttp_version(cls, ver):
        return cls(major=ver.major, minor=ver.minor)

    @classmethod
    def parse(cls, version):
        try:
            version = ensure_str(version)
            if version.startswith('HTTP/'):
                x, y = version[5:].split('.', 1)
                return cls(int(x), int(y))
        except ValueError:
            raise ValueError(f'invalid http version {version}')

    @classmethod
    def get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return cls.parse(v)
        elif isinstance(v, aiohttp.HttpVersion):
            return cls.from_aiohttp_version(v)
        elif isinstance(v, tuple):
            return cls(*v)
        raise ValueError(f'invalid http version {v}')




class URLRecord():
    """表示一个 URL 的记录类型。一般由爬虫发现输出。
    unique 条件应为 (url, request_method)"""

    url: str
    """链接的 url，不包含 query 及 fragment"""
    request_method: str
    """发现时请求方法"""
    response_status: int
    """发现时响应状态码"""
    response_content_type: str
    """发现时响应 content type"""

class VulnRecord():
    name: str
    type: str
    info: str
    level:str
    keyword: list
    target: str
    detail: str