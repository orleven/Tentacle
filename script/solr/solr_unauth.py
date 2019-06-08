#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'solr unauth'
        self.keyword = ['unauth', 'solr']
        self.info = 'solr unauth'
        self.type = 'unauth'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            for url in [self.base_url , self.base_url+"solr/"]:
                try:
                    res = self.curl('get',url)
                    if res and res.status_code is 200 and 'Solr Admin' in res.text and 'Dashboard' in res.text:
                        self.flag = 1
                        self.req.append({"page": '/solr/'})
                        self.res.append({"info": url, "key": "/solr/"})
                except Exception:
                    pass