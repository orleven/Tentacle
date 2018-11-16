#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import requests
import urllib.parse
requests.packages.urllib3.disable_warnings()

def get_script_info(data=None):
    script_info = {
        "name": "solr unauth",
        "info": "Solr unauth.",
        "level": "high",
        "type": "info",
    }
    return script_info

def prove(data):
    data = init(data, 'web')
    if data['url']:
        protocol, s1 = urllib.parse.splittype(data['url'])
        host, s2 = urllib.parse.splithost(s1)
        host, port = urllib.parse.splitport(host)
        port = port if data['target_port'] != None else 443 if protocol == 'https' else 80
        base_url = protocol + "://" + host +":"+str(port)
        for url in [base_url , base_url+"/solr/"]:
            try:
                res = requests.get(url, headers=data['headers'],verify=False,timeout=data['timeout'])
                if res.status_code is 200 and 'Solr Admin' in res.text and 'Dashboard' in res.text:
                    data['flag'] = 1
                    data['data'].append({"page": '/solr/'})
                    data['res'].append({"info": url, "key": "/solr/"})
            except Exception:
                pass
    return data


