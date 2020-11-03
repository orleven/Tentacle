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
        self.name = 'tomcat pages'
        self.keyword = ['web', 'tomcat']
        self.info = 'tomcat pages'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.INFO
        self.repair = ''
        self.refer = ''
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        await self.get_url()
        if self.base_url != None:
            async with ClientSession() as session:
                for url in [self.base_url, self.base_url + "docs/", self.base_url + "manager/",
                            self.base_url + "examples/",
                            self.base_url + "host-manager/"]:
                    async with session.get(url=url) as res:
                        if res:
                            text = await res.text()
                            if res.status == 200 and 'Apache Tomcat Examples' in text:
                                self.flag = 1
                                self.req.append({"page": 'tomcat page'})
                                self.res.append({"info": url, "key": "tomcat page"})
                            elif res.status == 401 and '401 Unauthorized' in text and 'tomcat' in text:
                                self.flag = 1
                                self.req.append({"page": 'tomcat page'})
                                self.res.append({"info": url, "key": "tomcat page"})
                            elif res.status == 403 and '403 Access Denied' in text and 'tomcat-users' in text:
                                self.flag = 1
                                self.req.append({"page": 'tomcat page'})
                                self.res.append({"info": url, "key": "tomcat page"})
                            elif res.status == 200 and 'Documentation' in text and 'Apache Software Foundation' in text and 'tomcat' in text:
                                self.flag = 1
                                self.req.append({"page": 'tomcat page'})
                                self.res.append({"info": url, "key": "tomcat page"})
