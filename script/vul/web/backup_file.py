#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

        self.extension_list = [
            ".dump", ".sql", ".sql.gz", ".sql.bz2", ".zip", ".gz", ".bz2", ".tar", ".rar",
            ".tar.gz", ".tar.bz2", ".7z", ".ini", ".cfg", ".sh", ".csv", ".bak",
        ]
        self.fix_length = 50

    async def prove(self):
        if self.base_url:
            vul_list = []
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/' and path.count('/') > 3:
                        try:
                            length1 = 0

                            key = '.isnotexist'
                            url = path[:-1] + key
                            async with session.get(url=url, allow_redirects=False) as res:
                                if res:
                                    text = await res.text()
                                    if text:
                                        length1 = len(text.replace('\\/', '/').replace(key, ''))

                            for extension in self.extension_list:
                                url = path[:-1] + extension
                                async with session.get(url=url, allow_redirects=False) as res:
                                    if res and res.status == 200:
                                        text = await res.text()
                                        if text:
                                            length = len(text.replace('\\/', '/').replace(extension, ''))
                                            if abs(length - length1) > self.fix_length:
                                                vul_list.append(url)

                                if len(vul_list) >= 3:
                                    return

                            for vul in vul_list:
                                yield vul
                        except:
                            pass
