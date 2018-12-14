#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

def info(data=None):
    info = {
        "name": "solr unauth",
        "info": "Solr unauth.",
        "level": "high",
        "type": "unauth",
    }
    return info

def prove(data):
    data = init(data, 'solr')
    if data['base_url']:
        for url in [data['base_url'] , data['base_url']+"solr/"]:
            try:
                res = curl('get',url)
                if res.status_code is 200 and 'Solr Admin' in res.text and 'Dashboard' in res.text:
                    data['flag'] = 1
                    data['data'].append({"page": '/solr/'})
                    data['res'].append({"info": url, "key": "/solr/"})
            except Exception:
                pass
    return data



if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))