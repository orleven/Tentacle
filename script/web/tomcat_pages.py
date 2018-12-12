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
    data = init(data,'web')
    if data['base_url']:
        data = _curl(data,data['base_url'])
    return data

def _curl(data,base_url):
    for url in [base_url, base_url + "docs/", base_url + "manager/", base_url + "examples/"]:
        try:
            flag = -1
            res = curl('get',url)
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
