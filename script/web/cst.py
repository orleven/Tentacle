#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import urllib.parse
import requests
requests.packages.urllib3.disable_warnings()

def info(data=None):
    info = {
        "name": "Cross Site Tracing (XST)",
        "info": "Cross Site Tracing (XST)",
        "level": "low",
        "type": "cst"
    }
    return info

def prove(data):
    data = init(data,'web')
    if data['url']:
        headers = {'fuck_by_me': 'hello_word'}
        try:
            res = curl('get',data['url'],headers = headers)
            if 'fuck_by_me' in res.headers.keys():
                data['flag'] = 1
                data['res'].append({"info": headers, "key": "cross_site_tracing (XST)"})
        except:
            pass
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))