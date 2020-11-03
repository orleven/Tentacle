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
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'wp-json unauth'
        self.keyword = ['web', 'wordpress']
        self.info = 'wp-json-unauth'
        self.type = VUL_TYPE.UNAUTH
        self.level = VUL_LEVEL.HIGH
        self.repair = ''
        self.refer = ''
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        await self.get_url()
        if self.base_url != None:
            async with ClientSession() as session:
                path_list = list(set([
                    self.url_normpath(self.base_url, './'),
                    self.url_normpath(self.url, './'),

                ]))
                file_list = ['wp-json', 'wp-json/wp/v2/users']
                for path in path_list:
                    for file in file_list:
                        url = path+file
                        async with session.get(url=url, allow_redirects=False, timeout=30) as res:
                            if res and res.status == 200:
                                text = await res.text()
                                text = text.lower()
                                if 'wp-json' in text and "description" in text and ('avatar_urls' in text or 'namespace' in text):
                                    self.flag = 1
                                    self.res.append({"info": url, "key": "wp-json-unauth"})
