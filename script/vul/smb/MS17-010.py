#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import binascii
from lib.util.aiohttputil import open_connection
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    MS17-010
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.SMB

    async def prove(self):
        if self.base_url is None:
            try:
                reader, writer = await open_connection(self.host, self.port)
                negotiate_protocol_request = binascii.unhexlify(
                    "00000054ff534d42720000000018012800000000000000000000000000002f4b0000c55e003100024c414e4d414e312e3000024c4d312e325830303200024e54204c414e4d414e20312e3000024e54204c4d20302e313200")
                session_setup_request = binascii.unhexlify(
                    "00000063ff534d42730000000018012000000000000000000000000000002f4b0000c55e0dff000000dfff02000100000000000000000000000000400000002600002e0057696e646f7773203230303020323139350057696e646f7773203230303020352e3000")
                try:
                    writer.write(negotiate_protocol_request)
                    await reader.read(1024)
                    writer.write(session_setup_request)
                    res = await reader.read(1024)
                    user_id = res[32:34]
                    tree_connect_andx_request = "000000%xff534d42750000000018012000000000000000000000000000002f4b%sc55e04ff000000000001001a00005c5c%s5c49504324003f3f3f3f3f00" % (
                    (58 + len(self.host)), user_id.hex(), bytes(self.port,'utf-8').hex())
                    writer.write(binascii.unhexlify(tree_connect_andx_request))
                    res = await reader.read(1024)
                    allid = res[28:36]
                    payload = "0000004aff534d422500000000180128000000000000000000000000%s1000000000ffffffff0000000000000000000000004a0000004a0002002300000007005c504950455c00" % allid.hex()
                    writer.write(binascii.unhexlify(payload))
                    res = await reader.read(1024)
                    if "\x05\x02\x00\xc0" in str(res):
                        yield "MS17-010"
                except:
                    pass
                finally:
                    writer.close()
            except:
                pass
