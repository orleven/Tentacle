#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from re import I
from re import findall
from re import search
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'cookie check'
        self.keyword = ['cookie', 'web']
        self.info = 'Check header\' cookies secure, e.g. httponly, secure and so on.'
        self.type = 'info'
        self.level = 'info'
        Script.__init__(self, target=target, server_type=self.server_type)

    def _plus(self, info,key = "cookie"):
        self.flag = 1
        self.res.append({"info": info, "key": key})

    def prove(self):
        self.get_url()
        if self.url:
            try:
                headers = self.curl('get',self.url).headers
                if 'cookies' in headers.keys():
                    cookies = headers['cookies'],
                    if not search(r'secure;', cookies, I):
                        self._plus('Cookie without Secure flag set')
                    if not search(r'httponly;', cookies, I):
                        self._plus( 'Cookie without HttpOnly flag set')
                    if search(r'domain\=\S*', cookies, I):
                        domain = findall(r'domain\=(.+?);', headers, I)
                        if domain:
                            self._plus( 'Session Cookie are valid only at Sub/Domain: %s' % domain[0])
                    if search(r'path\=\S*', cookies, I):
                        path = findall(r'path\=(.+?);', headers, I)
                        if path:
                            self._plus('Session Cookie are valid only on that Path: %s' % path[0])
                    if search(r'(.+?)\=\S*;', cookies, I):
                        cookie_sessions = findall(r'(.+?)\=\S*;', headers, I)
                        for cs in cookie_sessions:
                            if cs not in ['domain', 'path', 'expires']:
                                self._plus('Cookie Header contains multiple cookies')
                                break
                if 'x-xss-protection' not in headers.keys():
                    self._plus( 'X-XSS-Protection header missing','x-xss-protection')
                if 'x-frame-options' not in headers:
                    self._plus('Clickjacking: X-Frame-Options header missing','x-frame-options')
                if 'content-type' not in headers:
                    self._plus('Content-Type header missing','content-type')
                if 'strict-transport-security' not in headers:
                    self._plus('Strict-Transport-Security header missing','strict-transport-security')
                if 'x-content-type-options' not in headers:
                    self._plus('X-Content-Type-Options header missing','x-content-type-options')
            except :
                pass
