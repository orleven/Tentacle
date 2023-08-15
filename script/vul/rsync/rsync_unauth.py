#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import asyncio
from lib.util.aiohttputil import open_connection
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.RSYNC

    async def prove(self):
        if self.base_url is None:
            try:
                reader, writer = await open_connection(self.host, self.port)
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
                        reader1, writer1 = await open_connection(self.host, self.port)
                        message1 = '@RSYNCD: 30.0\r\n'
                        writer1.write(message1.encode())
                        data1 = (await reader1.read(1024)).decode('utf-8')
                        message1 = '{}\r\n'.format(line)
                        writer1.write(message1.encode())
                        res = (await reader1.read(1024)).decode('utf-8')
                        writer1.close()
                        if '@RSYNCD: OK' in res:
                            yield "rsync unauth"
            except:
                pass

