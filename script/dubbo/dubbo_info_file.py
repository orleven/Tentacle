#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.DUBBO
        self.name = 'dubbo info file'
        self.keyword = ['dubbo']
        self.info = 'dubbo info file'
        self.type = 'info'
        self.level = 'info'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.url:
            async with ClientSession() as session:
                urls = [
                    'dubbo-provider.xml',
                    'dubbo-cusmer.xml',
                ]
                for url in urls:
                    url = self.base_url + url
                    async with session.get(url=url) as response:
                        if response!=None:
                            text = await response.text()
                            if '<beans xmlns' in text:
                                self.flag = 1
                                self.res.append({"info": url, "key": 'dubbo info file'})

