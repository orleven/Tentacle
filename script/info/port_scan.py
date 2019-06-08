#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import socket
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.TOP100
        self.name = 'port scan'
        self.keyword = ['port', 'service']
        self.info = 'Get the open port and service'
        self.type = 'info'
        self.level = 'info'
        self.priority = 1
        Script.__init__(self, target=target, service_type=self.service_type,priority=self.priority)
        # super(POC, self).__init__(target=target,service_type=self.service_type)

    def prove(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message = None
        try:
            msg = "GET / HTTP/1.1\r\n\r\n"
            s.connect((self.target_host, self.target_port))
            s.sendall(bytes(msg, 'utf-8'))
            message = str(s.recv(100))
            self.flag = 2
        except Exception as e:
            message = str(e)
            flag = True
            for _ in ['WinError 10049', 'WinError 10061', 'timed out','getaddrinfo failed']:
                if _ in message:
                    flag = False
            if flag:
                if 'WinError 10054' not in message:
                    print(message,self.target_host,self.target_port)
                    self.flag = 2
        finally:
            s.close()
            if self.flag > -1:
                self.service_match(message)
                self.res.append({"info": self.service_type[0], "key": "port scan"})


    def service_match(self,message = None):
        self.get_url()
        if self.url:
            self.service_type = (SERVICE_PORT_MAP.WEB[0], self.target_port)
        elif message != None:
            pass