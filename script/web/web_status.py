#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import re
from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'web status'
        self.keyword = ['web', 'title', 'status']
        self.info = 'Get the web application status and title'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.INFO
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.url :
            async with ClientSession() as session:
                async with session.get(url=self.url) as response:
                    if response is not None :
                        res = await response.read()
                        status = response.status
                        try:
                            res = str(res, 'utf-8')
                        except UnicodeDecodeError:
                            try:
                               res = str(res, 'gbk')
                            except:
                                res = "[Error Code]"
                        except:
                            res = "[Error Code]"
                        m = re.search('<title>(.*)<\/title>', res.lower())
                        if m != None and m.group(1):
                            title = m.group(1)
                        else:
                            title = '[None Title]'
                        self.flag = 1
                        self.res.append({"info": title , "key": status, "status": status})