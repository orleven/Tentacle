#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import socket

def get_script_info(data=None):
    script_info = {
        "name": "dubbo unauth",
        "info": "This is a test.",
        "level": "medium",
        "type": "info",
    }
    return script_info


def prove(data):
    data = init(data,"dubbo")
    socket.setdefaulttimeout(data['timeout'])
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
