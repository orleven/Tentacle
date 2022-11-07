#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.SOLR

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for url in [self.base_url , self.base_url+"solr/"]:
                    async with session.get(url=url) as res:
                        if res and res.status == 200:
                            text = await res.text()
                            if 'Solr Admin' in text and 'Dashboard' in text:
                                yield url
                                break