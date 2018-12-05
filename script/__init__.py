#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import sys
import socks
import socket
import random
import requests
from requests import request
from lib.core.data import conf
from lib.core.data import logger
from requests.exceptions import ChunkedEncodingError, ConnectionError, ConnectTimeout,ReadTimeout
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



def get_ssh_key():
    try:
        public_key =  conf['config']['ssh_key']['public_key']
        private_key= conf['config']['ssh_key']['private_key']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: ssh_key, please check the config in tentacle.conf."))
    return public_key,private_key

def get_rebound():
    try:
        local_host =  conf['config']['rebound']['local_host']
        local_port= conf['config']['rebound']['local_port']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: rebound, please check the config in tentacle.conf."))
    return local_host,local_port

# def init_service(data):
#     # unknown，都来一遍
#     if data['service'] == None or data['service'].lower() in ["unknown",'tcpwrapped'] :
#         data['service'] = None
#
#     # http or https ，只扫web
#     elif 'http' in data['service']:
#         pass
#
#     # other，匹配到对应的就扫，匹配不到都来一遍
#     else:
#         for _service in service_table.keys():
#             if _service in data['service']:
#                 data['service'] = _service
#             else:
#                 data['service'] = None
#     return data
#
# def init(data,service):
#     data = init_service(data)
#     service = service.lower()
#     if data['service'] == None:
#         if data['target_port'] == None or int(data['target_port']) == 0:
#             if service in service_table.keys():
#                 data['target_port'] = service_table[service]
#             specal = 'api'
#
#
#     else:

def init(data,service='web'):
    service = service.lower()
    if data['target_port'] ==None or int(data['target_port']) == 0:
        if service in service_table.keys():
            data['target_port'] = service_table[service]

    if data['url'] == None:
        if service == 'web':
            for pro in ['http://', "https://"]:
                if int(data['target_port']) == 0:
                    if pro == 'http://':
                        data['target_port'] = 80
                    else:
                        data['target_port'] = 443
                url = pro + data['target_host'] + ":" +str(data['target_port']) + '/'
                data['url'] = head(data,url)
                if data['url']:
                    break
        elif service == 'http':
            if int(data['target_port']) == 0:
                data['target_port'] = 80
            url = "http://" +  data['target_host'] + ":" + str(data['target_port']) +'/'
            data['url'] = head(data,url)
        elif service == 'https':
            if int(data['target_port']) == 0:
                data['target_port'] = 443
            url = "https://" + data['target_host'] + ":" + str(data['target_port']) + '/'
            data['url'] = head(data,url)
        elif service == 'api':
            if int(data['target_port']) == 0:
                data['target_port'] = 80
                data['url'] = 'http://'+ data['target_host'] +'/'
            data['url'] = 'http://' + data['target_host'] + ":" +str(data['target_port']) +'/'

        if data['base_url'] == None:
            data['base_url'] = data['url']

    if conf['func_name'] == 'rebound':
        local_host,local_port = get_rebound()
        data['local_host'] = local_host
        data['local_port'] = local_port
    elif conf['func_name'] == 'sshkey':
        public_key, private_key = get_ssh_key()
        data['public_key'] = public_key
        data['private_key'] = private_key


    # sockrt proxy
    if conf['config']['proxy']['proxy'].lower() == 'true':
        try:
            socks5_host, socks5_port = conf['config']['proxy']['socks5'].split(':')
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, socks5_host, int(socks5_port))
            socket.socket = socks.socksocket
        except Exception as e:
            logger.error("Error socket proxy: %s" % conf['config']['proxy']['socks5'])
    socket.setdefaulttimeout(int(conf['config']['basic']['timeout']))

    return data


def head(data,url, params = None):
    s = curl('head',url, params)
    if s!= None:
        return url
    return s

def curl(method,url, params = None, **kwargs):
    headers = kwargs.get('headers')
    if headers == None:
        headers = {}
    headers["User-Agent"] = random.choice(conf['config']['basic']['user_agent'].split('\n'))
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    headers['Referer'] = url
    kwargs.setdefault('headers',headers)
    kwargs.setdefault('timeout',  int(conf['config']['basic']['timeout']))
    kwargs.setdefault('verify', False)

    if conf['config']['proxy']['proxy'].lower() == 'true':
        try:
            _proxies = {
                'http': conf['config']['proxy']['http_proxy'],
                'https': conf['config']['proxy']['https_proxy']
            }
            kwargs.setdefault('proxies', _proxies)
        except:
            logger.error("Error http(s) proxy: %s or %s." % (conf['config']['proxy']['http_proxy'],conf['config']['proxy']['https_proxy']))
    try:
        return request(method, url, params=params, **kwargs)
    except ConnectionError as e:
        # logger.error("ConnectionError: %s" % url)
        return None
    except ReadTimeout as e:
        # logger.error("ReadTimeout: %s" % url)
        return None
    except Exception as e:
        logger.error("Curl error: %s" % url)
        return None



