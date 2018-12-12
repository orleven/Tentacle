#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

'''
This is a example for script
'''

import time
import random
import requests
import socket


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
    # init(data,'web')
    # if data['url']:
    #     res = curl('get',data['url'])
    if random.randint(1, 100) > 99:
        data['flag'] = 1
        data['data'].append({})
        data['res'].append({"info": "", "key": ""})
        data['other'] = {}
    elif random.randint(1, 100) > 2:
        data['flag'] = -1
    else:
        data['flag'] = 0
    return data


def exec(data):
    # init(data,'smb')
    # if random.randint(1, 100) > 99:
    #     data['flag'] = 1
    #     data['data'].append({})
    #     data['res'].append({"info": "", "key": ""})
    #     data['other'] = {}
    # elif random.randint(1, 100) > 2:
    #     data['flag'] = -1
    # else:
    #     data['flag'] = 0
    return data


def rebound(data):
    # init(data,'smb')
    # if random.randint(1, 100) > 99:
    #     data['flag'] = 1
    #     data['data'].append({})
    #     data['res'].append({"info": "", "key": ""})
    #     data['other'] = {}
    # elif random.randint(1, 100) > 2:
    #     data['flag'] = -1
    # else:
    #     data['flag'] = 0
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
        "url": "",
        "base_url": "",
        "flag": "",

        "data": [],
        "res": [],
        "other": {},

        "local_host": "",
        "local_port": "",
    }
    from script import init
    from script import curl
    print(prove(init(data, 'http')))
