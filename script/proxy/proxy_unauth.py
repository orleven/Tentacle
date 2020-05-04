#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from aiohttp_socks import SocksConnector
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    '''
    因为aiohttp组件原因，暂无法支持检测https代理
    '''
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.PROXY
        self.name = 'proxy unauth'
        self.keyword = ['proxy']
        self.info = 'proxy unauth'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.LOWER
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        # socks proxy
        proxy = 'socks5://{}:{}'.format(self.target_host, str(self.target_port))
        connector = SocksConnector.from_url(proxy)
        url = 'http://example.com/'

        async with ClientSession(connector=connector) as session:
            async with session.get(url=url) as res1:
                if res1:
                    text1 = await res1.text()
                    if 'More information...' in text1:
                        self.flag = 1
                        self.res.append({"info": proxy, "key": "proxy unauth"})
                        return

        # http proxy
        proxy = 'http://{}:{}'.format(self.target_host, str(self.target_port))
        async with ClientSession() as session:
            async with session.get(url=url, proxy=proxy) as res2:
                if res2:
                    text2 = await res2.text()
                    if 'More information...' in text2:
                        self.flag = 1
                        self.res.append({"info": proxy, "key": "proxy unauth"})
                        return

