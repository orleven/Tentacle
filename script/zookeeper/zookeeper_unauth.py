#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import socket

def info(data=None):
    info = {
        "name": "zookeeper unauth",
        "info": "zookeeper unauth.",
        "level": "medium",
        "type": "unauth",
    }
    return info


def prove(data):
    data = init(data,'zookeeper')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((data['target_host'], data['target_port']))
        s.sendall(bytes('envi\r\n','utf-8'))
        message = str(s.recv(1024))
        s.close()
        if 'zookeeper.version' in message:
            data['flag'] = 1
            data['data'].append({"info": "envi"})
            data['res'].append({"info": "zookeeper unauth", 'key':'envi',"envi": message})
    except socket.timeout:
        pass
    except Exception as err:
        pass

    return data
