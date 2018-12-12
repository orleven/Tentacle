#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

def info(data=None):
    info = {
        "name": "http options",
        "info": "Http options.",
        "level": "low",
        "type": "info",
    }
    return info

def prove(data):
    data = init(data, 'web')
    if data['base_url'] != None:
        try:
            res = curl('options',data['base_url']+"/testbyme")
            allow = res.headers['Allow']
            data['flag'] = 1
            data['data'].append({"method": "options"})
            data['res'].append({"info": allow,"key":"OPTIONS"})
        except:
            pass
    return data
