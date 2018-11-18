#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import urllib.parse
import requests
requests.packages.urllib3.disable_warnings()

def get_script_info(data=None):
    script_info = {
        "name": "crossdomain",
        "info": "crossdomain.",
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
        url = base_url+'/crossdomain.xml'
        try:
            res = requests.get(url, headers=data['headers'], verify=False, timeout=data['timeout'])
            if 'allow-access-from domain="*"' in res.text:
                data['flag'] = 1
                data['data'].append({"page": '/crossdomain.xml'})
                data['res'].append({"info": url, "key": "/crossdomain.xml"})
        except:
            pass

    return data
