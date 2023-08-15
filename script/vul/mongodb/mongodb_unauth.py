#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import open_connection
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.MONGODB

    async def prove(self):
        if self.base_url is None:
            reader, writer = await open_connection(self.host, self.port)
            data = bytes.fromhex(
                "3a000000a741000000000000d40700000000000061646d696e2e24636d640000000000ffffffff130000001069736d6173746572000100000000")
            writer.write(data)
            result = await reader.read(1024)
            if "ismaster" in str(result):
                getlog_data = bytes.fromhex(
                    "480000000200000000000000d40700000000000061646d696e2e24636d6400000000000100000021000000026765744c6f670010000000737461727475705761726e696e67730000")
                writer.write(getlog_data)
                result1 = await reader.read(1024)
                if "totalLinesWritten" in str(result1):
                    yield f"mongodb_unauth"
            writer.close()