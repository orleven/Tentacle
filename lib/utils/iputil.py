#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re
import struct
from lib.core.data import logger

class CIDRHelper:
    def ip_format_chk(self, ip_str):
        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        if re.match(pattern, ip_str):
            return True
        else:
            return False

    def mask_len_chk(self, masklen):
        if masklen > 0 and masklen < 32:
            return True
        else:
            return False

    def parse(self, ip, masklen):
        if False == self.ip_format_chk(ip):
            return "0.0.0.1", "0.0.0.0"
        ips = ip.split(".")
        binip = 0
        for id in ips:
            binip = binip << 8
            binip += int(id)
        mask = (1 << 32) - 1 - ((1 << (32 - masklen)) - 1)
        a, b, c, d = struct.unpack('BBBB', struct.pack('>I', (binip & mask)))
        start = ".".join([str(a), str(b), str(c), str(d)])
        a, b, c, d = struct.unpack('BBBB', struct.pack('>I', (binip & mask) + (2 << (32 - masklen - 1)) - 1))
        end = ".".join([str(a), str(b), str(c), str(d)])
        return start, end

def build(start,end = None):
    hosts = []
    if start != None:
        if end !=None:
            for num in range(ip2num(start),ip2num(end)+1):
                hosts.append( num2ip(num))
        else:
            tmp = start.split('/')
            ch = CIDRHelper()
            start,end = ch.parse(tmp[0],int(tmp[1]))
            for num in range(ip2num(start),ip2num(end)+1):
                hosts.append( num2ip(num))
    return hosts

def ip2num(ip):
    lp = [int(x) for x in ip.split('.')]
    return lp[0] << 24 | lp[1] << 16 | lp[2] << 8 | lp[3]

def num2ip(num):
    ip = ['', '', '', '']
    ip[3] = (num & 0xff)
    ip[2] = (num & 0xff00) >> 8
    ip[1] = (num & 0xff0000) >> 16
    ip[0] = (num & 0xff000000) >> 24
    return '%s.%s.%s.%s' % (ip[0], ip[1], ip[2], ip[3])


def check_host(host):
    pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    match = pattern.match(host)
    if match:
        return True
    else:
        try:
            import socket
            socket.gethostbyname(host)
            return True
        except Exception as e:
            logger.error('Address error: %s' % host)
    return False

def check_domain(domain):
    try:
        import socket
        socket.gethostbyname(domain)
        return True
    except Exception as e:
        logger.error('Address error,%s' % domain)

def check_ip(ip):
    pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    match = pattern.match(ip)
    if match:
        return True
    return False


def check_ippool(ip):
    pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$')
    pattern1 = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if pattern.match(ip):
        return True
    elif pattern1.match(ip):
        return True
    return False

