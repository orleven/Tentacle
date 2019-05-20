#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'http options'
        self.keyword = ['web']
        self.info = 'http options'
        self.type = 'info'
        self.level = 'low'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.base_url != None:
            try:
                res = self.curl('options',self.base_url+"/testbyme")
                allow = res.headers['Allow']
                self.flag = 1
                self.req.append({"method": "options"})
                self.res.append({"info": allow,"key":"OPTIONS"})
            except:
                pass
