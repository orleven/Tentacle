#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'


def get_script_info(data=None):
    script_info = {
        "name": "memcache unauth",
        "info": "This is a test.",
        "level": "low",
        "type": "info",
        "author": "orleven",
        "url": "",
        "keyword": "tag:iis",
        "source": 1
    }
    return script_info



def prove(data):
    port = int(data['target_port']) if int(data['target_port']) != 0 else 11211
    data['target_port'] = port
    import socket,redis
    socket.setdefaulttimeout(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((data['target_host'], port))
        s.sendall(bytes('stats\r\n\r\nquit\r\n','utf-8'))
        message = str(s.recv(1024))
        s.close()
        if 'STAT' in message:
            data['flag'] = True
            data['data'].append({"info": "stats"})
            data['res'].append({"info": "The vul is exist!", "memcache_stats": message})
    except socket.timeout:
        pass
    except Exception as err:
        pass

    return data
