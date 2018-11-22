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
    if data['base_url']:
        for url in [data['base_url'] , data['base_url']+"solr/"]:
            try:
                res = requests.get(url, headers=data['headers'],verify=False,timeout=data['timeout'])
                if res.status_code is 200 and 'Solr Admin' in res.text and 'Dashboard' in res.text:
                    data['flag'] = 1
                    data['data'].append({"page": '/solr/'})
                    data['res'].append({"info": url, "key": "/solr/"})
            except Exception:
                pass
    return data


