#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import asyncio
import base64
import hashlib
import struct
from lib.core.env import *
from lib.util.aiohttputil import open_connection
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.RSYNC


    def load_dict(self):
        username_txt_path = self.parameter.get("U", None)
        if username_txt_path:
            self.username_list = self.read_file(username_txt_path)
        else:
            self.username_list = self.get_default_dict("rsync_usernames.txt")

        password_txt_path = self.parameter.get("P", None)
        if password_txt_path:
            self.password_list = self.read_file(password_txt_path)
        else:
            self.password_list = self.get_default_dict("rsync_passwords.txt")

    async def prove(self):
        if self.base_url is None:
            try:
                reader, writer = await open_connection(self.host, self.port)
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
                                yield result[0] + ':' + result[1] + ':' + result[2]
                else:
                    writer.close()
            except:
                pass

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

        async for (username, password) in self.generate_auth_dict(self.username_list, self.password_list):
            try:
                reader1, writer1 = await open_connection(self.host, self.port)
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
