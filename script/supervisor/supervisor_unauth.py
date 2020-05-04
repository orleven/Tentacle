#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.SUPERVISOR
        self.name = 'Supervisor unauth'
        self.keyword = ['supervisor']
        self.info = 'Supervisor unauth'
        self.type = VUL_TYPE.UNAUTH
        self.level = VUL_LEVEL.MEDIUM
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.url:
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
                            self.flag = 1
                            self.res.append({"info": 'supervisor_unauth', "key": 'supervisor unauth'})

