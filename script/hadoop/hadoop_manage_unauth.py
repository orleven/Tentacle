#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'hadoop_manage_unauth'
        self.keyword = ['hadoop', 'unauth']
        self.info = 'hadoop_manage_unauth'
        self.type = 'unauth'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            url = self.base_url + "node"
            async with ClientSession() as session:
                async with session.get(url=url) as res:
                    if res != None :
                        text = str(await res.read())
                        if 'Hadoop Version:' in text:
                            self.flag = 1
                            self.req.append({"url": url})
                            self.res.append({"info": url, "key": 'hadoop manage unauth'})