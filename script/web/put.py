#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import time

def info(data=None):
    info = {
        "name": "http put",
        "info": "Http put.",
        "level": "high",
        "type": "rec",
    }
    return info

def prove(data):
    data = init(data, 'web')
    if data['base_url'] != None:
        try:
            res = curl('options',data['base_url']+"/testbyme")
            allow = res.headers['Allow']
            if 'PUT' in allow:
                for _url in [str(int(time.time())) + '.jsp/',str(int(time.time())) + '.jsp::$DATA',str(int(time.time())) + '.jsp%20']:
                    url =  data['base_url'] + _url
                    res = curl('put', url)
                    if res.status == 201 or res.status == 204:
                        data['flag'] = 1
                        data['data'].append({"method": "put"})
                        data['res'].append({"info": url,"key":"PUT"})
        except:
            pass
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))