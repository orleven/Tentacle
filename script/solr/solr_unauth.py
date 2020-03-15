#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.SOLR
        self.name = 'solr unauth'
        self.keyword = ['unauth', 'solr']
        self.info = 'solr unauth'
        self.type = VUL_TYPE.UNAUTH
        self.level = VUL_LEVEL.MEDIUM
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                for url in [self.base_url , self.base_url+"solr/"]:
                    async with session.get(url=url) as res:
                        if res and res.status == 200:
                            text = await res.text()
                            if 'Solr Admin' in text and 'Dashboard' in text:
                                self.flag = 1
                                self.res.append({"info": url, "key": "solr unauth"})
                                break