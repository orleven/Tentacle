#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'



def get_script_info(data=None):
    script_info = {
        "name": "http options",
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


    headers = {}
    # port = int(data['target_port']) if int(data['target_port']) != 0 else 80
    if 'cookie' in data.keys():
        headers["Cookie"] = data['cookie']
    headers[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    import requests
    requests.packages.urllib3.disable_warnings()
    if 'url' in data.keys() and data['url'] != None:
        try:
            res = requests.options(data['url']+"/testbyme", headers=headers,verify=False, timeout=3)
            allow = res.headers['Allow']
            data['flag'] = True
            data['data'].append({"method": "options"})
            data['res'].append({"info": allow,"key":"OPTIONS"})
        except:
            pass
    else:
        if data['target_port'] == 0:
            target = data['target_host']
        else:
            target = data['target_host'] + ":" + str(data['target_port'])
        for pro in ['http://', "https://"]:
            try:
                res = requests.options(pro + target + "/testbyme", headers=headers, verify=False, timeout=3)
                allow = res.headers['Allow']
                data['flag'] = True
                data['url'] = pro + target
                data['data'].append({"method": "options"})
                data['res'].append({"info": allow, "key": "OPTIONS"})
            except:
                pass
    return data

