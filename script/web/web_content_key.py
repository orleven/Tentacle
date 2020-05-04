#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'web content key'
        self.keyword = ['web', 'title', 'keyword']
        self.info = 'Get the web application status and search keyword'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.INFO
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.url :
            async with ClientSession() as session:
                webkeydic = self.read_file(self.parameter['keyword'],'rb') if 'keyword' in self.parameter.keys() else self.read_file('dict/web_content_key.txt', 'rb')
                async with session.get(url=self.url) as response:
                    if response is not None :
                        res = await response.read()
                        try:
                            res = str(res, 'utf-8')
                        except UnicodeDecodeError:
                            res = str(res, 'gbk')
                        except:
                            res = "[Error Code]"
                        m = re.search('<title>(.*)<\/title>', res.lower())
                        if m != None and m.group(1):
                            title = m.group(1)
                        else:
                            title = '[None Title]'

                        key = ''
                        for searchkey in webkeydic:
                            searchkey = str(searchkey, 'utf-8').replace("\r", "").replace("\n", "")
                            try:
                                if searchkey in res:
                                    key += searchkey + ','
                                    self.flag = 1
                            except Exception as e:
                                print(e)
                                pass

                        if self.flag == 1:
                            self.res.append({"info": title, "key": key[:-1]})
