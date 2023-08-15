#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.GIILAB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        url = path + 'explore/projects'
                        try:
                            async with session.get(url=url) as res:
                                if res:
                                    text = await res.text()
                                    if res.status == 200 and 'GitLab' in text and 'Discover' in text:
                                        yield url
                        except:
                            pass
