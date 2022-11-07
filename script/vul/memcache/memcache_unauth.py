#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import open_connection
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.ZOOKEEPER


    async def prove(self):
        if not self.base_url:
            try:
                reader, writer = await open_connection(self.host, self.port)
                message = 'stats\r\n\r\nquit\r\n'
                writer.write(message.encode())
                data = await reader.read(1024)
                writer.close()
                if 'STAT ' in str(data):
                    yield "memcache unauth [stats]"
            except:
                pass