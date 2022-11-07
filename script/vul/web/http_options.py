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
            async with ClientSession() as session:
                for url in self.get_url_normpath_list(self.url, "./testbyme"):
                    if url[-1] == '/':
                        try:
                            async with session.options(url=url) as res:
                                if res != None and 'Allow' in res.headers:
                                    allow = res.headers['Allow']
                                    yield f"{url}   {allow}"
                                    return
                        except:
                            pass