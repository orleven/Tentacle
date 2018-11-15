#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'




def get_script_info(data):
    script_info = {
        "name": "This is a test.",
        "info": "This is a test.",
        "level": "low",
        "type": "info",
        "author": "orleven",
        "url": "",
        "keyword": "tag:iis",
        "source": 1
    }
    return script_info

def prove(data):
    '''
    data = {
        "target_host":"",
        "target_port":"",
        "proxy":"",
        "dic_one":"",
        "dic_two":"",
        "cookie":"",
        "url":"",
        "flag":"",
        "data":"",
        "":"",

    }
    '''

    import time
    import random
    res = {}
    time.sleep(3)
    if random.randint(1, 10) > 5:
        data['flag'] = True
    else :
        data['flag'] = False

    return data


def exec():
    data = {}
    data['data'] = 'This is a test.'
    import time
    import random
    if random.randint(1, 10) > 5:
        data['flag'] = True
    else:
        data['flag'] = False
    return data

