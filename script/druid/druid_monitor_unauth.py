#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'druid-monitor-unauth'
        self.keyword = ['web', 'druid']
        self.info = 'druid-monitor-unauth'
        self.type = VUL_TYPE.UNAUTH
        self.level = VUL_LEVEL.HIGH
        self.repair = ''
        self.refer = ''
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        await self.get_url()
        if self.base_url != None:
            async with ClientSession() as session:
                url = self.base_url + "druid/index.html"
                async with session.get(url=url, allow_redirects=False) as res:
                    if res and res.status == 200:
                        text = await res.text()
                        if 'Druid Stat Index' in text and "DruidVersion" in text:
                            self.flag = 1
                            self.res.append({"info": url, "key": "druid-monitor-unauth"})