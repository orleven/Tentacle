#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import open_connection
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.DUBBO
        self.name = 'dubbo unauth'
        self.keyword = ['dubbo','unauth']
        self.info = 'dubbo unauth'
        self.type = VUL_TYPE.UNAUTH
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        reader, writer = await open_connection(self.target_host, self.target_port)
        message = 'ls\r\n'
        writer.write(message.encode())
        data = str(await reader.read(1024))
        writer.close()
        if 'com.alibaba.dubbo' in data and ("token=false" in data or "token=true" not in data):
            self.flag = 1
            self.req.append({"info": "ls"})
            self.res.append({"info": "dubbo unauth", "key":"ls","dubbo_ls": data})
