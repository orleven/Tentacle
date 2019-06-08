#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'Cross Site Tracing (XST)'
        self.keyword = ['web']
        self.info = 'Cross Site Tracing (XST)'
        self.type = 'cst'
        self.level = 'low'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.url:
            headers = {'fuck_by_me': 'hello_word'}
            try:
                res = self.curl('get',self.url,headers = headers)
                if 'fuck_by_me' in res.headers.keys():
                    self.flag = 1
                    self.res.append({"info": headers, "key": "cross_site_tracing (XST)"})
            except:
                pass
