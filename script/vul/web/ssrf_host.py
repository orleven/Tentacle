#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    Host SSRF扫描
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            keyword = self.get_dnslog()
            headers = {
                'Host': keyword
            }
            url = self.base_url
            async with ClientSession() as session:
                try:
                    async with session.get(url, headers=headers) as res:
                        if res:
                            if await self.get_dnslog_recode(keyword):
                                yield url
                except:
                    pass