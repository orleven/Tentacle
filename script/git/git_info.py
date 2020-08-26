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
        self.service_type = SERVICE_PORT_MAP.DUBBO
        self.name = 'git info'
        self.keyword = ['git']
        self.info = 'git info'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.INFO
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.url:
            async with ClientSession() as session:
                urls = [
                    'explore/projects',
                ]
                for url in urls:
                    url = self.base_url + url
                    async with session.get(url=url) as response:
                        if response!=None:
                            text = await response.text()
                            if int(response.status) == 200 and 'GitLab' in text and 'Discover' in text:
                                self.flag = 1
                                self.res.append({"info": url, "key": 'git info'})

