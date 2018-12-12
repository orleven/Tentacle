#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import socket

def info(data=None):
    info = {
        "name": "dubbo unauth",
        "info": "dubbo unauth",
        "level": "medium",
        "type": "unauth",
    }
    return info


def prove(data):
    data = init(data,"dubbo")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((data['target_host'], data['target_port']))
        s.sendall(bytes('ls\r\n\r\n','utf-8'))
        message = str(s.recv(1024))
        s.close()
        if 'com.alibaba.dubbo' in message:
            data['flag'] = 1
            data['data'].append({"info": "ls"})
            data['res'].append({"info": "Dubbo unauth", "key":"ls","dubbo_ls": message})
    except socket.timeout:
        pass
    except Exception as err:
        pass

    return data
