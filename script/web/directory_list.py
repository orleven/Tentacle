#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import re
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'directory list'
        self.keyword = ['web']
        self.info = 'directory list'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.LOWER
        self.refer = 'https://github.com/WyAtu/Perun/blob/master/vuln/web/directory_listing.py'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            PAYLOADS = (
                re.compile(r'<title>Index of /', re.I),
                re.compile(r'<a href="?C=N;O=D">Name</a>', re.I),
                re.compile(r'<A HREF="?M=A">Last modified</A>', re.I),
                re.compile(r'Last modified</a>', re.I),
                re.compile(r'Parent Directory</a>', re.I),
                re.compile(r'<TITLE>Folder Listing.', re.I),
                re.compile(r'<table summary="Directory Listing', re.I),
                re.compile(r'">[To Parent Directory]</a><br><br>', re.I),
                re.compile(r'&lt;dir&gt; <A HREF="/', re.I),
                re.compile(r'''<pre><A HREF="/">\[''', re.I),
            )
            async with ClientSession() as session:
                path_list = list(set([
                    self.url_normpath(self.base_url, '/'),
                    self.url_normpath(self.url, './'),
                    self.url_normpath(self.url, '../'),
                ]))
                for path in path_list:
                    url = path
                    async with session.get(url=url) as response:
                        if response and response.status==200:
                            text = str(await response.read())
                            for payload in PAYLOADS:
                                r = payload.findall(text)
                                if r:
                                    self.flag = 1
                                    self.res.append({"info": url, "key": "directory_list"})
                                    return