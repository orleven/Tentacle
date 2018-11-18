#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import socket

def get_script_info(data=None):
    script_info = {
        "name": "zookeeper unauth",
        "info": "zookeeper unauth.",
        "level": "low",
        "type": "info",
    }
    return script_info



def prove(data):
    data = init(data,'zookeeper')
    socket.setdefaulttimeout(data['timeout'])
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
