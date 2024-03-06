#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven
import traceback

from lib.util.aiohttputil import open_connection
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.name = 'PortScan'
        self.service_type = ServicePortMap.UNKNOWN

    async def prove(self):

        if self.url is None:
            msg = "stats\r\n"
            try:
                reader, writer = await open_connection(host=self.host, port=self.port)
                writer.write(bytes(msg, 'utf-8'))
                await writer.drain()
            except:
                self.service = self.service_type[0]
            else:
                self.port_connect = True
                try:
                    message = await reader.read(1024)
                    self.service = await self.service_match(message)
                except Exception as e:
                    self.service = self.service_type[0]
                finally:
                    writer.close()

        else:
            await self.get_url()
            self.service = ServicePortMap.WEB[0]
        if self.url:
            if self.protocol is None:
                self.protocol = self.url[:self.url.index("://")]
            if self.base_url is None:
                self.base_url = f"{self.protocol}://{self.host}:{self.port}/"

        if self.port_connect:
            yield self.service
        else:
            if self.url is None:
                self.port_connect = False


    async def exec(self):
        yield self.prove()

    async def upload(self):
        yield self.prove()

    async def rebound(self):
        yield self.prove()

    async def service_match(self, message=None):

        await self.get_url()

        message = message.lower()

        if self.url:
            return ServicePortMap.WEB[0]

        elif message is not None:
            if b"amqp" in message:
                return ServicePortMap.RABBITMQ[0]
            elif b'smtp' in message or b'spam' in message or b'esmtp' in message or b'220 ******' in message:
                return ServicePortMap.SMTP[0]
            elif b'ssh' in message:
                return ServicePortMap.SSH[0]
            elif b'mysql' in message or b'caching_sha2_password' in message or b'mariadb' in message:
                return ServicePortMap.MYSQL[0]
            elif b'redis' in message or b'err wrong number of arguments for' in message or b'err unknown command' in message:
                return ServicePortMap.REDIS[0]
            elif b'FTP' in message or b'ftp' in message:
                return ServicePortMap.FTP[0]
            elif b'telnet' in message:
                return ServicePortMap.TELNET[0]
            elif b'rsync' in message or b'rsync' in message:
                return ServicePortMap.RSYNC[0]
            elif b'HTTP' in message or b'http' in message or b'\x15\x03\x03\x00\x02' in message or b'\x15\x03\x01\x00\x02' in message:
                return ServicePortMap.WEB[0]
            elif b'\xff\x00\x00\x00\x00\x00\x00\x00\x01\x7f' in message:
                return ServicePortMap.ZMTP[0]
            else:
                if b'' != message:
                    print(self.host, self.port, message)

        return ServicePortMap.UNKNOWN[0]


