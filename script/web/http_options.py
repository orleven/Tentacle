#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'http options'
        self.keyword = ['web']
        self.info = 'http options'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.INFO
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url != None:
            async with ClientSession() as session:
                for url in self.url_normpath(self.url, "./testbyme"):
                    async with session.options(url=url) as response:
                        if response!=None and 'Allow' in response.headers:
                            allow = response.headers['Allow']
                            self.flag = 1
                            self.req.append({"method": "options"})
                            self.res.append({"info": allow,"key":"OPTIONS"})
                            return