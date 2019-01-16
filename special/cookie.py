#!/usr/bin/env python 
# -*- coding:utf-8 -*-

'''
Check header' cookies secure, e.g. httponly, secure and so on.
'''

from re import findall
from re import search
from re import I

def info(data=None):
    info = {
        "name": "cookie",
        "info": "cookie",
        "level": "low",
        "type": "info"
    }
    return info

def _plus(data, info,key = "cookie"):
    data['flag'] = 1
    data['res'].append({"info": info, "key": key})
    return data

def prove(data):
    data = init(data, 'web')
    if data['url']:
        try:
            headers = curl('get',data['url']).headers
            if 'cookies' in headers.keys():
                cookies = headers['cookies'],
                if not search(r'secure;', cookies, I):
                    data = _plus(data,'Cookie without Secure flag set')
                if not search(r'httponly;', cookies, I):
                    data = _plus(data, 'Cookie without HttpOnly flag set')
                if search(r'domain\=\S*', cookies, I):
                    domain = findall(r'domain\=(.+?);', headers, I)
                    if domain:
                        data = _plus(data, 'Session Cookie are valid only at Sub/Domain: %s' % domain[0])
                if search(r'path\=\S*', cookies, I):
                    path = findall(r'path\=(.+?);', headers, I)
                    if path:
                        data = _plus(data, 'Session Cookie are valid only on that Path: %s' % path[0])
                if search(r'(.+?)\=\S*;', cookies, I):
                    cookie_sessions = findall(r'(.+?)\=\S*;', headers, I)
                    for cs in cookie_sessions:
                        if cs not in ['domain', 'path', 'expires']:
                            data = _plus(data, 'Cookie Header contains multiple cookies')
                            break
            if 'x-xss-protection' not in headers.keys():
                data = _plus(data, 'X-XSS-Protection header missing','x-xss-protection')
            if 'x-frame-options' not in headers:
                data = _plus(data, 'Clickjacking: X-Frame-Options header missing','x-frame-options')
            if 'content-type' not in headers:
                data = _plus(data, 'Content-Type header missing','content-type')
            if 'strict-transport-security' not in headers:
                data = _plus(data, 'Strict-Transport-Security header missing','strict-transport-security')
            if 'x-content-type-options' not in headers:
                data = _plus(data, 'X-Content-Type-Options header missing','x-content-type-options')
        except :
            pass
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'target_host':'www.baidu.com','target_port': 22,'flag':-1,'data':[],'res':[]}))