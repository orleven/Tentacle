#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'



def get_script_info(data=None):
    script_info = {
        "name": "solr unauth",
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
    import requests
    import urllib.parse
    requests.packages.urllib3.disable_warnings()
    protocol, s1 = urllib.parse.splittype(data['url'])
    host, s2 = urllib.parse.splithost(s1)
    host, port = urllib.parse.splitport(host)
    port = port if port != None else 443 if protocol == 'https' else 80
    base_url = protocol + "://" + host +":"+str(port)
    for url in [base_url , base_url+"/solr/"]:
        try:
            res = requests.get(url, headers=headers,verify=False)
            if res.status_code is 200 and 'Solr Admin' in res.text and 'Dashboard' in res.text:
                data['flag'] = True
                data['data'].append({"page": '/solr/'})
                data['res'].append({"info": url, "key": "/solr/"})
        except Exception:
            pass
    return data


