#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

from lib.utils.connect import open_connection
from script import Script, SERVICE_PORT_MAP, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.TOP150
        self.name = 'port scan'
        self.keyword = ['port', 'service']
        self.info = 'Get the open port and service'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.INFO
        self.repair = ''
        self.refer = ''
        self.priority = 1
        Script.__init__(self, target=target, service_type=self.service_type,priority=self.priority)
        # super(POC, self).__init__(target=target,service_type=self.service_type)

    async def prove(self):
        msg = "stats\r\n"
        self.flag = -1
        reader, writer = await open_connection(host=self.target_host,port=self.target_port)
        writer.write(bytes(msg, 'utf-8'))
        self.flag = 2
        await writer.drain()

        try:
            message = await reader.read(1024)
        except:
            message = None
        finally:
            writer.close()
        # self.flag = 2　
        if self.flag > -1:
            await self.service_match(message)
            self.res = [{"info": self.service_type[0], "key": "port scan"}]


    async def exec(self):
        await self.prove()

    async def upload(self):
        await self.prove()

    async def rebound(self):
        await self.prove()

    async def service_match(self,message = None):
        await self.get_url()
        if self.url:
            self.service_type = (SERVICE_PORT_MAP.WEB[0], self.target_port)
        elif message != None:
            message = str(message).lower()
            if 'smtp' in message and '220' in message:
                self.service_type = (SERVICE_PORT_MAP.SMTP[0], self.target_port)
            elif 'ssh' in message:
                self.service_type = (SERVICE_PORT_MAP.SSH[0], self.target_port)
            elif 'mysql' in message:
                self.service_type = (SERVICE_PORT_MAP.MYSQL[0], self.target_port)
            elif 'redis' in message or 'err wrong number of arguments for' in message or 'err unknown command' in message:
                self.service_type = (SERVICE_PORT_MAP.REDIS[0], self.target_port)
            elif "filezilla" in message or 'ftp' in message :
                self.service_type = (SERVICE_PORT_MAP.FTP[0], self.target_port)
            elif "rsync" in message:
                self.service_type = (SERVICE_PORT_MAP.RSYNC[0], self.target_port)
            elif "400 bad request" in message and "proxy" in message:
                self.flag = -1
            elif 'http' in  message:
                self.service_type = (SERVICE_PORT_MAP.WEB[0], self.target_port)
            else:
                self.service_type = (SERVICE_PORT_MAP.UNKNOWN[0], self.target_port)