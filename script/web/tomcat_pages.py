#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import urllib.parse
import requests
requests.packages.urllib3.disable_warnings()

def get_script_info(data=None):
    script_info = {
        "name": "tomcat pages",
        "info": "tomcat pages.",
        "level": "low",
        "type": "info"
    }
    return script_info

def prove(data):
    data = init(data,'web')
    if data['url']:
        protocol, s1 = urllib.parse.splittype(data['url'])
        host, s2 = urllib.parse.splithost(s1)
        host, port = urllib.parse.splitport(host)
        port = data['target_port'] if port != None else 443 if protocol == 'https' else 80
        base_url = protocol + "://" + host +":"+str(port)
        data = _curl(data,base_url, data['headers'],data['timeout'])
    return data

def _curl(data,base_url,headers,timeout):
    for url in [base_url, base_url + "/docs/", base_url + "/manager/", base_url + "/examples/"]:
        try:
            flag = -1
            res = requests.get(url, headers=headers, verify=False,timeout=timeout)
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
