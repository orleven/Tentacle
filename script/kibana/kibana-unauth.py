#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.ELASTICSEARCH
        self.name = 'kibana_unauth'
        self.keyword = ['kibana']
        self.info = 'kibana_unauth'
        self.type = VUL_TYPE.UNAUTH
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            if self.base_url != None:
                async with ClientSession() as session:
                    url = self.base_url + "app/kibana"
                    async with session.get(url=url, allow_redirects=False) as res:
                        if res and res.status == 200:
                            text = await res.text()
                            if 'kibanaWelcomeView' in text:
                                self.flag = 1
                                self.res.append({"info": url, "key": "kibana_unauth"})
