#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'tomcat pages'
        self.keyword = ['tomcat', 'web']
        self.info = 'tomcat pages'
        self.type = 'info'
        self.level = 'low'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            for url in [self.base_url, self.base_url + "docs/", self.base_url + "manager/", self.base_url + "examples/",
                        self.base_url + "host-manager/"]:
                try:
                    flag = -1
                    res = self.curl('get', url)
                    if res.status_code is 200 and 'Apache Tomcat Examples' in res.text:
                        flag = 1
                    elif res.status_code == 401 and '401 Unauthorized' in res.text and 'tomcat' in res.text:
                        flag = 1
                    elif res.status_code is 200 and 'Documentation' in res.text and 'Apache Software Foundation' in res.text:
                        flag = 1
                    if flag == 1:
                        self.flag = 1
                        self.req.append({"page": 'tomcat page'})
                        self.res.append({"info": url, "key": "tomcat page"})
                except Exception:
                    pass
