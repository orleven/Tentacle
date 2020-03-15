#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

from lib.utils.connect import open_connection
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.MONGODB
        self.name = 'mongodb unauth'
        self.keyword = ['mongodb', 'unauth']
        self.info = 'Check the mongodb unauthorized access'
        self.type = 'unauth'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        reader, writer = await open_connection(self.target_host, self.target_port)
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
                self.flag = 1
                self.res.append({"info": result1[:100], "key": "mongodb_unauth", "mongodb_info": result1})
        writer.close()