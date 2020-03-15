#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP, VUL_LEVEL, VUL_TYPE

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'Struts2-ongl-console'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-ongl-console'
        self.type = VUL_LEVEL.CRITICAL
        self.level = VUL_TYPE.RCE
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.url != None:
            async with ClientSession() as session:
                path_list = list(set([
                    self.url_normpath(self.base_url, '/'),
                    self.url_normpath(self.url, './'),
                ]))
                for path in path_list:
                    url = path + 'struts/webconsole.html'
                    async with session.get(url=url, allow_redirects=False) as res:
                        if res and res.status == 200 :
                            text = await res.text()
                            if 'OGNL console' in  text:
                                self.flag = 1
                                self.res.append({"info": self.url, "key": "Struts2-ongl-console"})
