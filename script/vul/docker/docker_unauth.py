#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.DOCKER


    async def prove(self):
        if self.base_url:
            url = self.base_url + 'containers/json'
            async with ClientSession() as session:
                try:
                    async with session.get(url=url) as res:
                        if res:
                            text = await res.text()
                            if 'docker' in text:
                                yield url
                except:
                    pass