#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import requests
requests.packages.urllib3.disable_warnings()

def get_script_info(data=None):
    script_info = {
        "name": "http options",
        "info": "Http options.",
        "level": "low",
        "type": "info",
    }
    return script_info

def prove(data):
    data = init(data, 'web')
    if data['url'] != None:
        try:
            res = requests.options(data['url']+"/testbyme", headers=data['headers'],verify=False, timeout=data['timeout'])
            allow = res.headers['Allow']
            data['flag'] = 1
            data['data'].append({"method": "options"})
            data['res'].append({"info": allow,"key":"OPTIONS"})
        except:
            pass
    return data
