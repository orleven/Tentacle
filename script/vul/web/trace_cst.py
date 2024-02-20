#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    Trace CST
    """
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB



    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for url in self.get_url_normpath_list(self.url, "./testbyme"):
                    headers = {
                        'test_cst': 'hello_world'
                    }
                    try:
                        async with session.request('Trace', url=url, headers=headers, allow_redirects=False) as res:
                            if res and 'test_cst' in res.headers.keys():
                                yield url
                    except:
                        pass
