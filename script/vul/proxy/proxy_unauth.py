#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from aiohttp_socks import SocksConnector
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    '''
    因为aiohttp组件原因，暂无法支持检测https代理
    '''
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.PROXY

    async def prove(self):
        url = 'http://example.com/'
        try:
            # socks proxy
            proxy = 'socks5://{}:{}'.format(self.host, str(self.port))
            connector = SocksConnector.from_url(proxy)
            async with ClientSession(connector=connector) as session:
                async with session.get(url=url) as res1:
                    if res1:
                        text1 = await res1.text()
                        if 'More information...' in text1:
                            yield proxy
        except:
            pass

        try:
            # http proxy
            proxy = 'http://{}:{}'.format(self.host, str(self.port))
            async with ClientSession() as session:
                async with session.get(url=url, proxy=proxy) as res2:
                    if res2:
                        text2 = await res2.text()
                        if 'More information...' in text2:
                            yield proxy
        except:
            pass
