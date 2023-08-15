#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.SUPERVISOR

    async def prove(self):
        if self.base_url:
            data = """<?xml version="1.0"?>
                <methodCall>
                <methodName>supervisor.getSupervisorVersion</methodName>
                </methodCall>
                """
            headers = {'Content-Type': 'application/xml'}
            url = self.base_url + 'RPC2'
            async with ClientSession() as session:
                async with session.post(url=url, data=data, headers=headers) as response:
                    if response != None:
                        text = str(await response.read())
                        if '<methodResponse>' in text:
                            yield url
