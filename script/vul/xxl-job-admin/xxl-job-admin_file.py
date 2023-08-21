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

        self.file_dic = {
            # nacos
            "xxl-job-admin/toLogin": "<a><b>XXL</b>JOB</a>",
        }

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == "/":
                        for file_path, file_keyword in self.file_dic.items():
                            url = path + file_path
                            async with session.get(url=url, allow_redirects=False) as res:
                                if res and res.status == 200:
                                    text = await res.text()
                                    if text and file_keyword in text.lower():
                                        yield url
