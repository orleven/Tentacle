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
        self.service_type = SERVICE_PORT_MAP.MECACHE
        self.name = 'memcache unauth'
        self.keyword = ['memcache', 'unauth']
        self.info = 'Memcache unauth.'
        self.type = VUL_TYPE.UNAUTH
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        reader, writer = await open_connection(self.target_host, self.target_port)
        message = 'stats\r\n\r\nquit\r\n'
        writer.write(message.encode())
        data = await reader.read(1024)
        writer.close()
        if 'STAT ' in str(data):
            self.flag = 1
            self.req.append({"info": "stats"})
            self.res.append({"info": "memcache unauth", "key": "stats", "memcache_stats": message})