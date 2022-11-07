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
                url = self.base_url + 'artifactory/ui/repodata?deploy=true'
                async with session.get(url=url, allow_redirects=False) as res:
                    if res and res.status == 200:
                        text = await res.text()
                        if 'repoKey' in text or 'repoTypesList' in text:
                            yield url