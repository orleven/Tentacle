#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.DOCKER
        self.name = 'docker unauth'
        self.keyword = ['unauth', 'docker']
        self.info = 'docker unauth'
        self.type = 'unauth'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            url = self.base_url + 'containers/json'
            res = self.curl('get', url)
            if res and 'docker' in res.text:
                self.flag = 1
                self.res.append({"info": url, "key": 'docker unauth'})