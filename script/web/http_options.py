#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP, VUL_TYPE, VUL_LEVEL

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
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            async with ClientSession() as session:
                for path in path_list:
                    async with session.options(url=path+"testbyme") as response:
                        if response!=None and 'Allow' in response.headers:
                            allow = response.headers['Allow']
                            self.flag = 1
                            self.req.append({"method": "options"})
                            self.res.append({"info": allow,"key":"OPTIONS"})