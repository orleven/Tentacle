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
                headers = {'fuck_by_me': 'hello_word'}
                for url in self.get_url_normpath_list(self.url):
                    try:
                        async with session.get(url=url, headers=headers) as res:
                            if res and 'fuck_by_me' in res.headers.keys():
                                yield url
                    except:
                        pass