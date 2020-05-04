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
        self.name = 'crossdomain'
        self.keyword = ['web']
        self.info = 'crossdomain'
        self.vul_type = VUL_TYPE.INFO
        self.vul_level = VUL_LEVEL.INFO
        self.refer = 'Basic script'
        self.repair = 'Basic script'
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
                    url = path+ "crossdomain.xml"
                    async with session.options(url=url) as response:
                        if response!=None:
                            text = await response.text()
                            if 'domain="*"' in text:
                                self.flag = 1
                                self.res.append({"info": url, "key":"crossdomain"})
                                return