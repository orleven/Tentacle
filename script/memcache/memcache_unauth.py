#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import socket

def info(data=None):
    info = {
        "name": "memcache unauth",
        "info": "Memcache unauth.",
        "level": "high",
        "type": "unauth",
    }
    return info

def prove(data):
    data = init(data,'memcache')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((data['target_host'], data['target_port']))
        s.sendall(bytes('stats\r\n\r\nquit\r\n','utf-8'))
        message = str(s.recv(1024))
        s.close()
        if 'STAT ' in message:
            data['flag'] = 1
            data['data'].append({"info": "stats"})
            data['res'].append({"info": "memcache unauth", "key":"stats","memcache_stats": message})
    except socket.timeout:
        pass
    except Exception as err:
        pass
    return data


if __name__=='__main__':
    from script import init, curl
    print(prove({'target_host':'www.baidu.com','target_port': 22,'flag':-1,'data':[],'res':[]}))