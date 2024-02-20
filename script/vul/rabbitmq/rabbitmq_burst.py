#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.core.env import *
from base64 import b64encode
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.RABBITMQ

    def load_dict(self):
        username_txt_path = self.parameter.get("U", None)
        if username_txt_path:
            self.username_list = self.read_file(username_txt_path)
        else:
            self.username_list = self.get_default_dict("rabbitmq_usernames.txt")

        password_txt_path = self.parameter.get("P", None)
        if password_txt_path:
            self.password_list = self.read_file(password_txt_path)
        else:
            self.password_list = self.get_default_dict("rabbitmq_passwords.txt")

    async def prove(self):
        if self.base_url:
            url = self.base_url + 'api/whoami'
            async with ClientSession() as session:
                async with session.get(url=url) as res:
                    if res and res.status == 401:
                        async for (username, password) in self.generate_auth_dict(self.username_list, self.password_list):
                            try:
                                key = str(b64encode(bytes(":".join([username, password]), 'utf-8')), 'utf-8')
                                headers = {"Authorization": 'Basic %s' % key}
                                async with session.get(url=url, headers=headers) as res1:
                                    if res1 and res1.status != 401:
                                        text1 = await res1.text()
                                        if 'Console' in text1 or (username in text1 and 'name' in text1) or 'auth_backend' in text1:
                                            yield username + "/" + password
                            except:
                                pass

