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
            pocs = ["is_not_exist"]
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url, ['./public/', './']):
                    if path[-1] == '/':
                        for poc in pocs:
                            url = path + poc
                            async with session.get(url=url) as res:
                                if res != None:
                                    text = await res.text()
                                    if 'Environment Variables' in text:
                                       yield url
                                       
