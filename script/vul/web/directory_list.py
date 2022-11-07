#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import re
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    敏感文件泄露扫描
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for url in self.get_url_normpath_list(self.url):
                    if url[-1] == '/':
                        try:
                            async with session.get(url=url, allow_redirects=False) as res:
                                if res and res.status == 200:
                                    content = await res.text()
                                    flag = False
                                    if '<title>Index of' in content and '<h1>Index of' in content:
                                        flag = True
                                    if '<title>Directory listing' in content:
                                        flag = True
                                    if '[To Parent Directory]</A>' in content and '</H1><hr>' in content:
                                        flag = True
                                    if '.bash_history' in content and ".bash_profile" in content:
                                        flag = True
                                    if 'etc' in content and "var" in content and 'sbin' in content and 'tmp' in content:
                                        flag = True

                                    test_num = 0
                                    lines = re.findall('<a href="(.*)">(.*)</a>', content, re.IGNORECASE)
                                    for href, value in lines:
                                        if href == value:
                                            test_num += 1
                                        if test_num > 3:
                                            flag = True
                                            break

                                    if flag:
                                        yield url
                        except:
                            pass