#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    hadoop_manage_unauth
    """
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            url = self.base_url + "node"
            async with ClientSession() as session:
                async with session.get(url=url) as res:
                    if res != None :
                        text = str(await res.read())
                        if 'Hadoop Version:' in text:
                            yield url