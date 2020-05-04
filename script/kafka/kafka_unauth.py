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
        self.name = 'kafka_unauth'
        self.keyword = ['kafka','unauth']
        self.info = 'kafka_unauth'
        self.type = VUL_TYPE.UNAUTH
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                async with session.get(url=self.base_url) as res:
                    if res != None:
                        text = await res.text()
                        if 'Kafka Manager' in text:
                            self.flag = 1
                            self.req.append({"url": self.url})
                            self.res.append({"info": self.url, "key": 'kafka unauth'})