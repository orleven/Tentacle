#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import requests
import urllib.parse
requests.packages.urllib3.disable_warnings()

service_table = {
    "ftp": 21,
    "ssh": 22,
    "telnet": 23,
    "smtp": 25,
    "dns": 53,
    "http": 80,
    "rpc": 110,
    "netbios": 139,
    "ldap": 389,
    "https": 443,
    "smb": 445,
    "imap": 993,
    "rsync": 873,
    "sqlserver": 1433,
    "oracle": 1521,
    "zookeeper": 2181,
    "mysql": 3306,
    "rdp": 3389,
    "postgresql": 5432,
    "vnc": 5900,
    "redis": 6379,
    "elasticsearch": 9200,
    'memcache': 11211,
    "dubbo": 20880,
    "mongodb": 27017,
}

public_key = '''ssh-rsa ====='''

private_key = """
-----BEGIN RSA PRIVATE KEY-----
=====
-----END RSA PRIVATE KEY-----
    """

def init(data,service='web'):
    # data['timeout'] = 4

    service = service.lower()
    if int(data['target_port']) == 0:
        if service in service_table.keys():
            data['target_port'] = service_table[service]
    # try:
    #     if int(data['target_port']) == 0 :
    #         if service in service_table.keys():
    #             data['target_port'] = service_table[service]
    #         else:
    #             data['target_port'] = 80
    # except:
    #     data['target_port'] = 80
    headers = {}
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    if data['url'] == None:
        if service == 'web':
            for pro in ['http://', "https://"]:
                if int(data['target_port']) == 0:
                    if pro == 'http://':
                        data['target_port'] = 80
                    else:
                        data['target_port'] = 443
                data['url'] = curl_status(pro, data['target_host'], data['target_port'], headers,data['timeout'])
                if data['url']:
                    break
        elif service == 'http':
            if int(data['target_port']) == 0:
                data['target_port'] = 80
            data['url'] = curl_status("http://", data['target_host'], data['target_port'], headers,data['timeout'])
        elif service == 'https':
            if int(data['target_port']) == 0:
                data['target_port'] = 443
            data['url'] = curl_status("https://", data['target_host'], data['target_port'], headers,data['timeout'])
        elif service == 'api':
            if int(data['target_port']) == 0:
                data['target_port'] = 80
                data['url'] = 'http://'+ data['target_host']
            data['url'] = 'http://' + data['target_host'] + ":" +str(data['target_port'])

    if data['url'] :
        headers['Referer'] = data['url']
        data['headers'] = headers
        protocol, s1 = urllib.parse.splittype(data['url'])
        host, s2 = urllib.parse.splithost(s1)
        host, port = urllib.parse.splitport(host)
        port = data['target_port'] if port != None else 443 if protocol == 'https' else 80
        data['base_url'] = protocol + "://" + host + ":" + str(port) +'/'
    return data

def curl_status(pro, host,port,headers,timeout):
    target = pro + host + ":" + str(port)
    try:
        requests.head(target, headers=headers, verify=False, timeout=timeout)
        return target
    except:
        pass
    return None