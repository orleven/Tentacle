#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import socket
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.MECACHE
        self.name = 'memcache unauth'
        self.keyword = ['memcache', 'unauth']
        self.info = 'Memcache unauth.'
        self.type = 'unauth'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)


    def prove(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.target_host, self.target_port))
            s.sendall(bytes('stats\r\n\r\nquit\r\n','utf-8'))
            message = str(s.recv(1024))
            s.close()
            if 'STAT ' in message:
                self.flag = 1
                self.req.append({"info": "stats"})
                self.res.append({"info": "memcache unauth", "key":"stats","memcache_stats": message})
        except socket.timeout:
            pass
        except Exception as err:
            pass