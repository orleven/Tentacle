#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'Cross Site Tracing (XST)'
        self.keyword = ['web']
        self.info = 'Cross Site Tracing (XST)'
        self.type = VUL_TYPE.CST
        self.level = VUL_LEVEL.LOW
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.url:
            headers = {'fuck_by_me': 'hello_word'}
            async with ClientSession() as session:
                async with session.get(url=self.url,headers = headers) as response:
                    if response!=None and 'fuck_by_me' in response.headers.keys():
                        self.flag = 1
                        self.res.append({"info": 'fuck_by_me', "key": 'fuck_by_me'})

