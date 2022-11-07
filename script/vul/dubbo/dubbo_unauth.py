#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import open_connection
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.DUBBO

    async def prove(self):
        if self.base_url is None:
            reader, writer = await open_connection(self.host, self.port)
            message = 'ls\r\n'
            writer.write(message.encode())
            data = str(await reader.read(1024))
            writer.close()
            if 'com.alibaba.dubbo' in data and ("token=false" in data or "token=true" not in data):
                yield f"dubbo unauth [ls]"