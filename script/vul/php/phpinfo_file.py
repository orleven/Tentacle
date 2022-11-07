#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB
        self.file_list = [
            "phpinfo.php",
            "info.php",
            "index.php",
            "test.php",
            "php.php",
            "p.php",
            "1.php",
            "a.php",
            "debug.php",
            "dashboard/phpinfo.php",
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
                                        text_source = await res.text()
                                        text = text_source.lower()
                                        if 'phpinfo()' in text:
                                            yield url
                            except:
                                pass
