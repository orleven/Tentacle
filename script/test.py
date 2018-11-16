#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

"""
    This is a test for script.
"""

import time
import random


def info(data):
    """
    Get script module's info.
    :param data:
    :return:
    """
    info = {
        "name": "Test",
        "info": "This is a test.",
        "level": "low",
        "type": "info",
        "keyword": "test",
        "source": 1
    }
    return info

def prove(data):
    """
    Prove vul(default choice)
    :param data:
    :return:
    """
    init(data, 'http')
    time.sleep(1)
    if random.randint(1, 10) > 7:
        data['flag'] = 1
    elif random.randint(1, 10) > 5:
        data['flag'] = -1
    else:
        data['flag'] = 0
    data['res'].append({})
    data['data'].append({})
    data['other'] = {}
    return data


def exec(data):
    time.sleep(1)
    if random.randint(1, 10) > 7:
        data['flag'] = True
    elif random.randint(1, 10) > 5:
        return data
    else:
        data['flag'] = False
    data['res'].append({})
    data['data'].append({})
    data['other'] = {}
    return data


def rebound(data):
    data = init(data, 'web')
    if data['url'] != None:  # for web
        time.sleep(0.5)
    else:
        time.sleep(1)
    # print(data["dic_one"])
    if random.randint(1, 10) > 7:
        data['flag'] = True
    elif random.randint(1, 10) > 5:
        return data
    else:
        data['flag'] = False
    data['res'].append({})
    data['data'].append({})
    data['other'] = {}
    return data

def _test(data):
    """
    Example for private function, and can't show.
    :param data:
    :return:
    """
    return data


if __name__ == '__main__':

    data = {
        "target_host": "",
        "target_port": "",

        "proxy": "",
        "dic_one": "",
        "dic_two": "",
        "cookie": "",
        "url": "",
        "flag": "",

        "data": [],
        "res": [],
        "other": {},

        "local_host": "",
        "local_port": "",
    }
    import sys
    sys.path.append("..")
    from script import init
    print(prove(init(data, 'http')))
