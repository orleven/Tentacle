#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import urllib.parse
import requests
requests.packages.urllib3.disable_warnings()

def info(data=None):
    info = {
        "name": "crossdomain",
        "info": "crossdomain.",
        "level": "low",
        "type": "info"
    }
    return info

def prove(data):
    data = init(data,'web')
    if data['base_url']:
        url = data['base_url']+'crossdomain.xml'
        try:
            res = curl('get',url)
            if 'allow-access-from domain="*"' in res.text:
                data['flag'] = 1
                data['data'].append({"page": '/crossdomain.xml'})
                data['res'].append({"info": url, "key": "/crossdomain.xml"})
        except:
            pass

    return data
