#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import aioping
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.name = 'PingScan'
        self.service_type = ServicePortMap.UNKNOWN


    async def prove(self):
        try:
            delay = await aioping.ping(self.host)
            if delay is not None:
                yield "Ping"
        except:
            pass

    async def exec(self):
        yield self.prove()

    async def upload(self):
        yield self.prove()

    async def rebound(self):
        yield self.prove()
