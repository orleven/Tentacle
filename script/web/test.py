#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import re

def get_script_info(data=None):
    script_info = {
        "name": "This is a test.",
        "info": "This is a test.",
        "level": "low",
        "type": "info",
        "author": "orleven",
        "url": "",
        "keyword": "test",
        "source": 1
    }
    return script_info

def prove(data):
    '''
    data = {
        "target_host":"",
        "target_port":"",
        "local_host":"",
        "local_port":"",
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
    # print(data["dic_one"])
    if random.randint(1, 10) > 5:
        data['flag'] = True
    else :
        data['flag'] = False
    return data


def exec(data=None):
    data = {}
    data['data'] = 'This is a test.'
    import time
    import random
    if random.randint(1, 10) > 5:
        data['flag'] = True
    else:
        data['flag'] = False
    return data


def rebound(data):

    return data

def _test(data):
    """
    Example for private function, and can't show.
    :param data:
    :return:
    """
    return data