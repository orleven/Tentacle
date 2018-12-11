#!/usr/bin/evn python
# -*- coding: utf-8 -*-
import socket
import json
import time


def assign(service, arg):
    if service == 'www' and _G["find_service"]:
        url_info = urlparse.urlparse(arg)
        try:
            hostname = socket.gethostbyname(url_info.netloc)
            return True, hostname
        except:
            return False

def prove(data):
    try:
        hostname = socket.gethostbyname(data['target_host'])
    except:
        return data
    info = hostname
    data['flag'] = 1
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % hostname
    while True:
        try:
            res = curl('get', url)
            if res.status_code == 200:
                jsondata = json.loads(res.text)
                if jsondata['code'] == 1:
                    jsondata['data'] = {'region': '', 'city': '', 'isp': ''}
                else:
                    if jsondata['data']['region']:
                        info += " | Region: " + jsondata['data']['region']
                    if jsondata['data']['isp']:
                        info += " | ISP: " + jsondata['data']['isp']
                    if jsondata['data']['city']:
                        info += " | City: " + jsondata['data']['city']
                break
            elif res.status_code == 502:
                time.sleep(0.3)
            else:
                break
        except :
            pass
    data['res'].append({"info": info, "key": 'IP Information'})
    return data