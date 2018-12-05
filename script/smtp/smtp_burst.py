#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import time,socket,re,base64

def info(data=None):
    info = {
        "name": "smtp burst",
        "info": "smtp burst.",
        "level": "high",
        "type": "weakpass",
    }
    return info

def prove(data):
    data = init(data, 'smtb')
    if _socket_connect(data['target_host'], data['target_port']):
        usernamedic = _read_dic(data['dic_one']) if 'dic_one' in data.keys() else  _read_dic('dict/smtp_usernames.txt')
        passworddic = _read_dic(data['dic_two']) if 'dic_two' in data.keys() else  _read_dic('dict/smtp_passwords.txt')
        for linef1 in usernamedic:
            username = linef1.strip('\r').strip('\n')
            for linef2 in passworddic:
                password = (
                    linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                    '\r').strip('\n')
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((data['target_host'], data['target_port']))
                    banner = str(s.recv(1024))
                    emailaddress = '.'.join(data['target_host'].split('.')[1:])
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
                                        data['flag'] = 1
                                        data['data'].append({"username": username, "password": password})
                                        data['res'].append({"info": username + "/" + password, "key": 'smtp'})
                                        return data
                except:
                    pass
    return data


# def exec(data=None):
#     data = {}
#     data['data'] = 'This is a test.'
#     import time
#     import random
#     if random.randint(1, 10) > 10:
#         data['flag'] = True
#     else:
#         data['flag'] = False
#     return data

def _read_dic(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()
def _socket_connect(ip, port,msg = "test"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(ip, port)
        s.sendall(bytes(msg, 'utf-8'))
        message = str(s.recv(1024))
        s.close()
        return True
    except:
        return False
