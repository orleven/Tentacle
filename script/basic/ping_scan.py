#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import ping3
from lib.util.aiohttputil import open_connection
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.name = 'PingScan'
        self.service_type = ServicePortMap.UNKNOWN


    async def prove(self):
        try:
            response_time = ping3.ping(self.host)
            if response_time is not None:
                yield "Ping"
        except:
            pass

    async def exec(self):
        yield self.prove()

    async def upload(self):
        yield self.prove()

    async def rebound(self):
        yield self.prove()
