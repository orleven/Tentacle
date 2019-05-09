#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

def info(data=None):
    info = {
        "name": "tomcat pages",
        "info": "tomcat pages.",
        "level": "low",
        "type": "info"
    }
    return info

def prove(data):
    data = init(data,'tomcat')
    if data['base_url']:
        for url in [data['base_url'], data['base_url'] + "docs/", data['base_url'] + "manager/", data['base_url'] + "examples/",
                    data['base_url'] + "host-manager/"]:
            try:
                flag = -1
                res = curl('get', url)
                if res.status_code is 200 and 'Apache Tomcat Examples' in res.text:
                    flag = 1
                elif res.status_code == 401 and '401 Unauthorized' in res.text and 'tomcat' in res.text:
                    flag = 1
                elif res.status_code is 200 and 'Documentation' in res.text and 'Apache Software Foundation' in res.text:
                    flag = 1
                if flag == 1:
                    data['flag'] = 1
                    data['data'].append({"page": 'tomcat page'})
                    data['res'].append({"info": url, "key": "tomcat page"})
            except Exception:
                pass
    return data


if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))