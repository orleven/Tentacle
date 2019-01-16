#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import sys
import socks
import socket
from lib.core.data import conf
from lib.core.data import logger
from lib.utils.curl import mycurl
from lib.core.data import engine
from lib.api.api import _ceye_dns_api
from lib.api.api import _ceye_verify_api

service_table = {
    "ftp": 21,
    "ssh": 22,
    "telnet": 23,
    "smtp": 25,
    "dns": 53,
    "http": 80,
    "rpc": 110,
    "pop3": 110,
    "netbios": 139,
    "ldap": 389,
    "https": 443,
    "smb": 445,
    "rsync": 873,
    "imap": 993,
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

def init(data,service='web'):
    # Don't have url and port
    service = service.lower()
    if data['target_port'] == None or int(data['target_port']) == 0:
        if service in service_table.keys():
            data['target_port'] = service_table[service]

    # Don't have url but have port
    if data['url'] == None:
        if service == 'api':
            data['url'] = data['base_url'] = 'http://' + data['target_host'] + ":" +str(data['target_port']) +'/'
        else:
            data['url'], data['target_host'], data['target_port'] = geturl(data['target_host'], data['target_port'])
            data['base_url'] = data['url']

    if conf['func_name'] == 'rebound':
        local_host,local_port = get_rebound()
        data['local_host'] = local_host
        data['local_port'] = local_port
    elif conf['func_name'] == 'sshkey':
        public_key, private_key = get_ssh_key()
        data['public_key'] = public_key
        data['private_key'] = private_key

    # socket proxy
    if conf['config']['proxy']['proxy'].lower() == 'true':
        try:
            socks5_host, socks5_port = conf['config']['proxy']['socks5'].split(':')
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, socks5_host, int(socks5_port))
            socket.socket = socks.socksocket
        except Exception as e:
            logger.error("Error socket proxy: %s" % conf['config']['proxy']['socks5'])
    socket.setdefaulttimeout(int(conf['config']['basic']['timeout']))
    return data

def curl(method,url, params = None, **kwargs):
    return mycurl(method,url, params = params, **kwargs)

def load_targets(target,service=None):
    engine._load_target(target,service = service)

def geturl(host, port, params = None, **kwargs):
    for pro in ['http://', "https://"]:
        _port = port if port != None and port != 0 else 443 if pro == 'https' else 80
        _pro = 'https://' if port == 443 else pro
        url = _pro + host + ":" + str(_port) + '/'
        res = mycurl('head',url, params, **kwargs)
        if res != None :
            if res.status_code == 400 and 'The plain HTTP request was sent to HTTPS port' in res.text:
                continue
            return url,host,_port
    return None,host,port

def get_ssh_key():
    try:
        public_key = conf['config']['ssh_key']['public_key']
        private_key = conf['config']['ssh_key']['private_key']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: ssh_key, please check the config in tentacle.conf."))
    return public_key,private_key

# def get_rebound():
#     try:
#         local_host = conf['config']['rebound']['local_host']
#         local_port = conf['config']['rebound']['local_port']
#     except KeyError:
#         sys.exit(logger.error("Load tentacle config error: rebound, please check the config in tentacle.conf."))
#     return local_host,local_port

def ceye_dns_api(t = 'url'):
    '''
    curl ssrf
    :param t:
    :return:
    '''
    return _ceye_dns_api(t = t)

def ceye_verify_api(filter, t = 'dns'):
    '''
    verify ssrf
    :param filter:
    :param t:
    :return:
    '''
    return _ceye_verify_api(filter = filter, t = t)

