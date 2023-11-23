#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import aiosmtplib
from lib.core.env import *
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.SSH

    def load_dict(self):
        username_txt_path = self.parameter.get("U", None)
        if username_txt_path:
            self.username_list = self.read_file(username_txt_path)
        else:
            self.username_list = self.get_default_dict("smtp_usernames.txt")

        password_txt_path = self.parameter.get("P", None)
        if password_txt_path:
            self.password_list = self.read_file(password_txt_path)
        else:
            self.password_list = self.get_default_dict("smtp_passwords.txt")

    async def prove(self):
        if self.base_url is None:
            try:
                async for (username, password) in self.generate_auth_dict(self.username_list, self.password_list):
                    if self.port == 465:
                        use_tls = True
                    else:
                        use_tls = False
                    try:
                        async with aiosmtplib.SMTP(hostname=self.host, port=self.port, use_tls=use_tls, timeout=self.timeout) as smtp:
                            await smtp.login(username, password,  timeout=self.timeout)
                            yield username + "/" + password
                            
                    except aiosmtplib.SMTPAuthenticationError:
                          pass
            except:
                pass