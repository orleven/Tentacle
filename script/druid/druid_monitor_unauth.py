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
                path_list = list(set([
                    self.url_normpath(self.base_url, 'druid/'),
                    self.url_normpath(self.base_url, 'console.html'),
                    self.url_normpath(self.url, './'),

                ]))
                for path in path_list:
                    async with session.get(url=path, allow_redirects=False) as res:
                        if res and res.status == 200:
                            text = await res.text()
                            text = text.lower()
                            if 'druid stat index' in text or "druidversion" in text or 'druid indexer' in text:
                                self.flag = 1
                                self.res.append({"info": path, "key": "druid-monitor-unauth"})