#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import re
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for url in self.get_url_normpath_list(self.url):
                    try:
                        async with session.get(url=url) as res:
                            if res:
                                status = res.status
                                try:
                                    body = await res.read()
                                    res = str(body, 'utf-8')
                                except UnicodeDecodeError:
                                    try:
                                        res = str(body, 'gbk')
                                    except:
                                        res = "[Error Code]"
                                except:
                                    res = "[Error Code]"
                                m = re.search('<title>(.*)<\/title>', res, re.IGNORECASE)
                                if m and m.group(1):
                                    title = m.group(1)
                                else:
                                    title = '[None Title]'
                                yield f"{url}   {title} [{status}]"
                    except:
                        pass