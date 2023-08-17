#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

"""
在原aiohttp上封装一层，便于请求的控制
"""

import json
import traceback
import aiohttp
import aiohttp_socks
from lib.core.env import *
from yarl import URL
from typing import Any
from typing import Union
from typing import Type
from typing import Optional
from types import TracebackType
from yarl._quoting_py import _Quoter
from yarl._quoting_py import UNRESERVED
from aiohttp.client import hdrs
from aiohttp.client import TCPConnector
from aiohttp.client import _RequestContextManager
from aiohttp.client_exceptions import asyncio
from aiohttp.client_exceptions import ServerDisconnectedError
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.client_exceptions import ClientResponseError
from aiohttp.client_exceptions import ClientOSError
from aiohttp.client_exceptions import TooManyRedirects
from asyncio.exceptions import IncompleteReadError
from asyncio.exceptions import TimeoutError
from python_socks._errors import ProxyConnectionError
from python_socks._errors import ProxyError
from lib.core.g import log
from lib.core.g import conf
from lib.util.util import random_ua
from lib.util.util import ip_header

def open_connection(host, port, **kwargs):
    # 因为 aiohttp 组件原因，暂无法支持检测https代理, 因此弃用http/https代理，统一使用socks5代理
    try:
        if conf.proxy.proxy == True:
            proxy_url = conf.proxy.proxy_url
            return aiohttp_socks.open_connection(socks_url=proxy_url, host=host, port=port, **kwargs)
    except KeyError as e:
        log.error("Load tentacle config error: %s, please check the config in tentacle.conf." %e)
    return asyncio.open_connection(host=host, port=port, **kwargs)

class ClientSession(aiohttp.ClientSession):
    """
    重写ClientSession的_request函数，功能与原相同
    """

    def __init__(self, max_retries=0, retry_interval=5, max_fail_redirects=3, **kwargs):
        """
        :param retry_interval: 重试间隔
        :param max_retries: 重试次数
        :param max_fail_redirects: 抛出TooManyRedirects错误后，重定向次数
        :param kwargs:
        """

        if kwargs.get('connector') is None:
            connector = TCPConnector(ssl=False)
            try:
                if conf.proxy.proxy == True:
                    proxy_url = conf.proxy.proxy_url
                    connector = aiohttp_socks.SocksConnector.from_url(proxy_url)
            except KeyError as e:
                log.error("Load tentacle config error: %s, please check the config in tentacle.conf." % e)
            kwargs.setdefault('connector', connector)

        self.__max_data_queue_num = conf.basic.max_data_queue_num
        self.__max_retries = max_retries if max_retries >= 0 else 0
        self.__retry_interval = retry_interval
        self.__max_fail_redirects = max_fail_redirects
        self.__qps_limit = conf.scan.scan_qps_limit
        super().__init__(**kwargs)

    def request(self, method: str, url: Union[str, URL], **kwargs: Any) -> "RequestContextManager":
        """Perform HTTP request."""
        if not kwargs.get('read_until_eof', True):
            return RequestContextManager(super()._request(method, url, **kwargs))
        return RequestContextManager(self._request(method, url, **kwargs))

    def get(self, url: Union[str, URL], *, allow_redirects: bool = True, **kwargs: Any) -> "RequestContextManager":
        """Perform HTTP GET request."""
        return RequestContextManager(self._request(hdrs.METH_GET, url, allow_redirects=allow_redirects, **kwargs))

    def options(self, url: Union[str, URL], *, allow_redirects: bool = True, **kwargs: Any) -> "RequestContextManager":
        """Perform HTTP OPTIONS request."""
        return RequestContextManager(self._request(hdrs.METH_OPTIONS, url, allow_redirects=allow_redirects, **kwargs))

    def head(self, url: Union[str, URL], *, allow_redirects: bool = False, **kwargs: Any) -> "RequestContextManager":
        """Perform HTTP HEAD request."""
        return RequestContextManager(self._request(hdrs.METH_HEAD, url, allow_redirects=allow_redirects, **kwargs))

    def post(self, url: Union[str, URL], *, data: Any = None, **kwargs: Any) -> "RequestContextManager":
        """Perform HTTP POST request."""
        return RequestContextManager(self._request(hdrs.METH_POST, url, data=data, **kwargs))

    def put(self, url: Union[str, URL], *, data: Any = None, **kwargs: Any) -> "RequestContextManager":
        """Perform HTTP PUT request."""
        return RequestContextManager(self._request(hdrs.METH_PUT, url, data=data, **kwargs))

    def patch(self, url: Union[str, URL], *, data: Any = None, **kwargs: Any) -> "RequestContextManager":
        """Perform HTTP PATCH request."""
        return RequestContextManager(self._request(hdrs.METH_PATCH, url, data=data, **kwargs))

    def delete(self, url: Union[str, URL], **kwargs: Any) -> "RequestContextManager":
        """Perform HTTP DELETE request."""
        return RequestContextManager(self._request(hdrs.METH_DELETE, url, **kwargs))

    async def _request(self, method, url, keyword: str = None, **kwargs):
        """
        重写_request函数，功能与原相同， 增加默认代理等配置
        """

        # 关闭ssl验证
        kwargs.setdefault('verify_ssl', False)

        # 增加默认ua
        headers = kwargs.get('headers', {})
        user_agent = headers.get("User-Agent", 'aiohttp')
        if 'aiohttp' in user_agent:
            try:
                for key, value in conf.scan.scan_headers.items():
                    if isinstance(key, str) and isinstance(value, str):
                        headers[key] = value
            except:
                headers["User-Agent"] = random_ua()

        # 设置timeout
        if kwargs.get('timeout') is None:
            kwargs.setdefault('timeout', conf.scan.scan_timeout)

        # 增加X-Forwarded-For等字段
        if 'API-Key' not in headers.keys():
            for key, value in ip_header().items():
                if key not in headers.keys():
                    headers[key] = value

        # 设置cookie
        cookie = headers.get("Cookie", None)
        if isinstance(cookie, dict):
            headers['Cookie'] = '; '.join(['='.join([key, value]) for key, value in cookie.items()])

        # 设置headers
        kwargs.setdefault('headers', headers)

        if kwargs.get('proxy') is None:
            if conf.support.hasattr("support_proxy"):
                if MAIN_NAME != 'simple':
                    kwargs.setdefault('proxy', conf.support.support_proxy)

        data = b''
        total = self.__max_retries + 1
        for count in range(total):
            if count > 0:
                log.warning(f'Request to {url} failed, retrying ({count} / {total})...')
            else:
                log.debug(f'Request to {url}')

            try:
                resp = await super()._request(method, url, **kwargs)
                # 临时加入request_content参数，便于数据包存储
                json_data = kwargs.get('json', None)
                if json_data:
                    data = json.dumps(json_data)
                else:
                    data = kwargs.get('data', None)
                if data:
                    if isinstance(data, str):
                        data = bytes(data, 'utf-8')
                else:
                    data = b''
                resp.__dict__['request_content'] = data
                return resp
            except TooManyRedirects:
                kwargs.setdefault('allow_redirects', False)
                kwargs.setdefault('max_redirects', self.__max_fail_redirects)
                return await self._request(method, url, **kwargs)
            except (TimeoutError, ClientOSError, ClientResponseError, IncompleteReadError,
                    ClientConnectorError, ServerDisconnectedError, ConnectionResetError, AttributeError,
                    ProxyConnectionError, RuntimeError, OSError, BrokenPipeError, ProxyError):
                pass
            except Exception as e:
                err = str(e).strip()
                if err != '' and 'InvalidServerVersion' not in err and 'Unexpected SOCKS' not in err:
                    traceback.print_exc()
                    log.error(f"Error request, url: {url}, error: {err}")
            await asyncio.sleep(self.__retry_interval)

        return None

class RequestContextManager(_RequestContextManager):

    __slots__ = ()

    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Optional[TracebackType],) -> None:
        if self._resp is not None:
            self._resp.release()

# 修复 aithttp 默认解码的问题
URL._PATH_REQUOTER = _Quoter(safe="@:", protected=UNRESERVED + "/+")
