#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                url = self.base_url+ '*~1*/.aspx'
                try:
                    async with session.get(url=url) as res1:
                        if res1:
                            url = self.base_url + 'l1j1e*~1*/.aspx'
                            async with session.get(url=url) as res2:
                                if res2:
                                    if res1.status == 404 and res2.status == 400:
                                        yield url
                except:
                    pass