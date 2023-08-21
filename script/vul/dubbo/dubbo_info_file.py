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
        if self.url:
            async with ClientSession() as session:
                poc_list = [
                    'dubbo-provider.xml',
                    'dubbo-cusmer.xml',
                ]
                for poc in poc_list:
                    url = self.base_url + poc
                    async with session.get(url=url) as response:
                        if response!=None:
                            text = await response.text()
                            if '<beans xmlns' in text:
                                yield url


