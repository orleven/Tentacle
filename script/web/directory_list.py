#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import re
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'directory list'
        self.keyword = ['web']
        self.info = 'directory list'
        self.type = 'info'
        self.level = 'medium'
        self.refer = 'https://github.com/WyAtu/Perun/blob/master/vuln/web/directory_listing.py'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
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
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            for path in path_list:
                url = path
                res = self.curl('get', url)
                if res and res==200:
                    for payload in PAYLOADS:
                        r = payload.findall(res.text)
                        if r:
                            self.flag = 1
                            self.res.append({"info": url, "key": "directory_list"})
                            return