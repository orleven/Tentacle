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
        else:
            data['url'] = data['base_url'] = geturl(data['target_host'], data['target_port'])

    # Don't have url but have port
    if data['url'] == None:
        if service in service_table.keys() or service in ['http','web','https']:
            data['url'] = data['base_url'] = geturl(data['target_host'], data['target_port'])
        elif service == 'api':
            data['url'] = data['base_url'] =  'http://' + data['target_host'] + ":" +str(data['target_port']) +'/'

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
        port = port if port != None or port != 0 else 443 if pro == 'https' else 80
        url = pro + host + ":" + str(port) + '/'
        res = mycurl('head',url, params, **kwargs)
        if res!= None:
            return url
    return None

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




