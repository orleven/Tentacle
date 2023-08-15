#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    Tomcat 敏感文件泄露扫描
    """
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB
        self.file_list = [
            "host-manager/",
            "manager/html",
            "examples/",
            "docs/",
            "",
        ]

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        for file_path in self.file_list:
                            try:
                                url = path + file_path
                                async with session.get(url=url, allow_redirects=False) as res:
                                    if res and res.status == 200:
                                        text = await res.text()
                                        if res.status == 200 and 'Apache Tomcat Examples' in text:
                                            yield url
                                        elif res.status == 401 and '401 Unauthorized' in text and 'tomcat' in text:
                                            yield url
                                        elif res.status == 403 and '403 Access Denied' in text and 'tomcat-users' in text:
                                            yield url
                                        elif res.status == 200 and 'Documentation' in text and 'Apache Software Foundation' in text and 'tomcat' in text:
                                            yield url
                            except:
                                pass
