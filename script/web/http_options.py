#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'http options'
        self.keyword = ['web']
        self.info = 'http options'
        self.type = 'info'
        self.level = 'low'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url != None:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            for path in path_list:
                try:
                    res = self.curl('options',path+"/testbyme")
                    allow = res.headers['Allow']
                    self.flag = 1
                    self.req.append({"method": "options"})
                    self.res.append({"info": allow,"key":"OPTIONS"})
                except:
                    pass
