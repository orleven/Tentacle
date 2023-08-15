#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import aiomysql
from lib.core.env import *
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.MYSQL


    def load_dict(self):
        username_txt_path = self.parameter.get("U", None)
        if username_txt_path:
            self.username_list = self.read_file(username_txt_path)
        else:
            self.username_list = self.get_default_dict("mysql_usernames.txt")

        password_txt_path = self.parameter.get("P", None)
        if password_txt_path:
            self.password_list = self.read_file(password_txt_path)
        else:
            self.password_list = self.get_default_dict("mysql_passwords.txt")


    async def prove(self):
        if self.base_url is None:
            async for (username, password) in self.generate_auth_dict(self.username_list, self.password_list):
                try:
                    async with aiomysql.create_pool(host=self.host, port=self.port, user=username,
                                                    password=password, timeout=self.timeout) as res:
                        yield username + "/" + password
                        return
                except Exception:
                    pass

