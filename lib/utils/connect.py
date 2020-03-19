#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import ssl
import traceback
import aiohttp
import random
import aiohttp_socks
from typing import Any
from aiohttp_socks import SocksConnector
from aiohttp.client_exceptions import asyncio
from aiohttp.client_exceptions import ServerDisconnectedError
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.client_exceptions import ClientResponseError
from aiohttp.client_exceptions import ClientOSError
from aiohttp.client_exceptions import TooManyRedirects
from aiohttp.client import _BaseRequestContextManager
from aiohttp.client import TCPConnector
from aiohttp.typedefs import StrOrURL
from lib.core.data import conf
from lib.core.data import logger
from lib.core.settings import USER_AGENTS
from lib.core.common import random_IP
from lib.core.common import get_safe_ex_string

def open_connection(host, port, **kwargs):
    # 因为 aiohttp 组件原因，暂无法支持检测https代理, 因此弃用http/https代理，统一使用socks5代理
    try:
        if conf['proxy']['proxy'].lower() == 'true':
            proxy_url = conf['proxy']['proxy_url']
            return aiohttp_socks.open_connection(socks_url=proxy_url, host=host, port=port, **kwargs)
    except KeyError as e:
        logger.error("Load tentacle config error: %s, please check the config in tentacle.conf." %e )
    return asyncio.open_connection(host=host, port=port, **kwargs)

class _RequestContextManager(_BaseRequestContextManager):
    async def __aexit__(self, exc_type, exc, tb):
        if self._resp!=None:
            self._resp.release()

class ClientSession(aiohttp.ClientSession):
    def __init__(self, retry_interval=5, max_qps=None, **kwargs):
        if kwargs.get('connector') is None:
            # 因为 aiohttp 组件原因，暂无法支持检测https代理, 因此弃用http/https代理，统一使用socks5代理
            try:
                if conf['proxy']['proxy'].lower() == 'true':
                    proxy = conf['proxy']['proxy_url']
                    connector = SocksConnector.from_url(proxy)
                else:
                    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
                    connector = TCPConnector(ssl=False)
                kwargs.setdefault('connector', connector)
            except KeyError as e:
                logger.error("Load tentacle config error: %s, please check the config in tentacle.conf." % e)

        self._max_fail_retries = int(conf['basic']['max_retries']) or 0
        self._retry_interval = retry_interval
        self._limit = LimitRate(1, 1. / max_qps) if max_qps else None
        super().__init__(**kwargs)

    async def _request(self, method, url, **kwargs):
        headers = kwargs.get('headers')
        if headers == None:
            headers = {}

        if 'Accept' not in headers.keys() :
            headers["Accept"] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'

        if 'Accept-Charset' not in headers.keys() :
            headers["Accept-Charset"] = 'GB2312,utf-8;q=0.7,*;q=0.7'

        if 'Accept-Encoding' not in headers.keys() :
            # headers["Accept-Encoding"] = 'gzip, deflate, sdch, br'
            headers["Accept-Encoding"] = 'gzip, deflate, sdch'

        headers['Referer'] = url
        if 'User-Agent' not in headers.keys() or 'aiohttp' in headers["User-Agent"] :
            headers["User-Agent"] = random.choice(USER_AGENTS)

        # random_ip = random_IP()
        # if 'Client_IP' not in headers.keys():
        #     headers['Client_IP'] = random_ip
        # if 'X-Forwarded-For' not in headers.keys():
        #     headers['X-Forwarded-For'] = random_ip

        kwargs.setdefault('headers', headers)
        kwargs.setdefault('verify_ssl',False)

        if self._limit:
            await self._limit.wait_available()
        total = self._max_fail_retries if method.lower() == 'get' else 0

        timeout = int(conf['basic']['timeout'])

        if 'timeout' not in kwargs.keys():
            kwargs.setdefault('timeout', timeout)

        # if kwargs.get('proxy') is None:
        #     try:
        #         if True:
        #             proxy = 'http://localhost:8080/'
        #             kwargs.setdefault('proxy', proxy)
        #     except KeyError as e:
        #         logger.error("Load tentacle config error: %s, please check the config in tentacle.conf." % e)

        for count in range(total):
            resp = None
            try:
                resp = await super()._request(method, url, **kwargs)
                return resp
            except Exception as ex:
                pass
            logger.warning('request to {url} failed, retrying ({count} / {total})...')
            if resp:
                resp.close()
            await asyncio.sleep(self._retry_interval)
        try:
            return await super()._request(method, url, **kwargs)
        except TooManyRedirects:
            kwargs.setdefault('max_redirects', 3)
            try:
                return await self._request(method, url, **kwargs)
            except:
                return None
        except (ClientOSError, ClientResponseError, ClientConnectorError, ServerDisconnectedError):
            return None
        except Exception as e:
            if get_safe_ex_string(e).strip() != '' and 'InvalidServerVersion' not in get_safe_ex_string(e) and 'Unexpected SOCKS' not in get_safe_ex_string(e):
                # errmsg = traceback.format_exc()
                # logger.error(errmsg)
                logger.error("Curl error: %s for %s" % (get_safe_ex_string(e), url))
            return None

    def get(self, url: StrOrURL, *, allow_redirects: bool=True,
            **kwargs) -> '_RequestContextManager':
        """Perform HTTP GET request."""
        return _RequestContextManager(self._request(aiohttp.hdrs.METH_GET, url,
                          allow_redirects=allow_redirects,
                          **kwargs))

    def options(self, url: StrOrURL, *, allow_redirects: bool=True,
                **kwargs) -> '_RequestContextManager':
        """Perform HTTP OPTIONS request."""
        return _RequestContextManager(
            self._request(aiohttp.hdrs.METH_OPTIONS, url,
                          allow_redirects=allow_redirects,
                          **kwargs))

    def head(self, url: StrOrURL, *, allow_redirects: bool=False,
             **kwargs) -> '_RequestContextManager':
        """Perform HTTP HEAD request."""
        return _RequestContextManager(
            self._request(aiohttp.hdrs.METH_HEAD, url,
                          allow_redirects=allow_redirects,
                          **kwargs))

    def post(self, url: StrOrURL,
             *, data: Any=None, **kwargs) -> '_RequestContextManager':
        """Perform HTTP POST request."""
        return _RequestContextManager(
            self._request(aiohttp.hdrs.METH_POST, url,
                          data=data,
                          **kwargs))

    def put(self, url: StrOrURL,
            *, data: Any=None, **kwargs) -> '_RequestContextManager':
        """Perform HTTP PUT request."""
        return _RequestContextManager(
            self._request(aiohttp.hdrs.METH_PUT, url,
                          data=data,
                          **kwargs))

    def patch(self, url: StrOrURL,
              *, data: Any=None, **kwargs) -> '_RequestContextManager':
        """Perform HTTP PATCH request."""
        return _RequestContextManager(
            self._request(aiohttp.hdrs.METH_PATCH, url,
                          data=data,
                          **kwargs))

    def delete(self, url: StrOrURL, **kwargs) -> '_RequestContextManager':
        """Perform HTTP DELETE request."""
        return _RequestContextManager(
            self._request(aiohttp.hdrs.METH_DELETE, url,
                          **kwargs))

class LimitRate:
    def __init__(self, count, duration):
        self._count = count
        self._duration = duration
        self._slots = []
        self._loop = asyncio.get_event_loop()

    async def wait_available(self):
        while len(self._slots) >= self._count:
            first = self._slots[0]
            delta = self._duration - (self._loop.time() - first)
            if delta < 0:
                self._slots.pop(0)
            else:
                await asyncio.sleep(delta)
        self._slots.append(self._loop.time())
