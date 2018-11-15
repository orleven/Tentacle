#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'



def get_script_info(data=None):
    script_info = {
        "name": "tomcat pages",
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

    import socket
    socket.setdefaulttimeout(5)
    headers = {}
    headers[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

    import urllib.parse

    if 'url' in data.keys() and data['url'] != None:
        protocol, s1 = urllib.parse.splittype(data['url'])
        host, s2 = urllib.parse.splithost(s1)
        host, port = urllib.parse.splitport(host)
        port = port if port != None else 443 if protocol == 'https' else 80
        base_url = protocol + "://" + host +":"+str(port)
        data = _curl(data,base_url, headers)
    else:
        if data['target_port'] == 0:
            target = data['target_host']
        else:
            target = data['target_host'] + ":" + str(data['target_port'])
        for pro in ['http://', "https://"]:

            if _curl_status(data,pro + target, headers):
                data = _curl(data,pro + target, headers)
    return data

def _curl_status(data,base_url,headers):
    import requests
    requests.packages.urllib3.disable_warnings()
    try:
        requests.get(base_url, headers=headers, verify=False, timeout=5)
        return True
    except:
        return False

def _curl(data,base_url,headers):
    import requests
    requests.packages.urllib3.disable_warnings()
    for url in [base_url, base_url + "/docs/", base_url + "/manager/", base_url + "/examples/"]:
        try:
            flag = False
            res = requests.get(url, headers=headers, verify=False,timeout=5)
            if res.status_code is 200 and 'Apache Tomcat Examples' in res.text:
                flag = True
            elif res.status_code == 401 and '401 Unauthorized' in res.text and 'tomcat' in res.text:
                flag = True
            elif res.status_code is 200 and 'Documentation' in res.text and 'Apache Software Foundation' in res.text:
                flag = True
            if flag:
                data['flag'] = True
                data['data'].append({"page": 'tomcat page'})
                data['res'].append({"info": url, "key": "tomcat page"})
        except Exception:
            pass
    return data
