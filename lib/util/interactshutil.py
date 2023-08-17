#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# based on https://github.com/ElSicarius/interactsh-python/blob/main/sources/interactsh.py

import json
import base64
import random
from uuid import uuid4
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import PKCS1_OAEP
from lib.core.g import log
from lib.util.aiohttputil import ClientSession

server_list = ["oast.pro", "oast.live", "oast.site", "oast.online", "oast.fun", "oast.me"]

class Interactsh:
    def __init__(self):
        self.server = None
        self.domain = None
        self.correlation_id = None
        self.custom_server = None
        self.token = None

    def config(self, server, token):
        self.custom_server = server
        self.token = token

    async def register(self):
        rsa = RSA.generate(1024)

        self.public_key = rsa.publickey().exportKey()
        self.private_key = rsa.exportKey()

        encoded_public_key = base64.b64encode(self.public_key).decode("utf8")

        uuid = uuid4().hex.ljust(33, "a")
        guid = "".join(i if i.isdigit() else chr(ord(i) + random.randint(0, 20)) for i in uuid)

        self.correlation_id = guid[:20]
        self.secret = str(uuid4())
        headers = {}

        if self.custom_server:
            if not self.token:
                log.error("Interact.sh token is not set")
            headers["Authorization"] = self.token
            self.server_list = [self.custom_server]
        else:
            self.server_list = random.sample(server_list, k=len(server_list))
        for server in self.server_list:
            log.info(f"Registering with interact.sh server: {server}")
            data = {
                "public-key": encoded_public_key,
                "secret-key": self.secret,
                "correlation-id": self.correlation_id,
            }
            data = json.dumps(data)
            url = f"https://{server}/register"
            try:
                async with ClientSession() as session:
                    async with session.request("POST", url, data=data, headers=headers) as res:
                        if res is None:
                            continue
                        text = await res.json()

                        msg = text.get("message", "")
                        if "registration successful" not in msg:
                            continue
            except:
                log.debug(f"Failed to register with interactsh server {self.server}")
            self.server = server

            self.domain = f"{guid}.{self.server}"
            break

        if not self.server:
            log.error(f"Failed to register with an interactsh server")

        log.info(
            f"Successfully registered to interactsh server {self.server} with correlation_id {self.correlation_id} [{self.domain}]"
        )

        return self.domain

    async def deregister(self):
        if not self.server or not self.correlation_id or not self.secret:
            log.error(f"Missing required information to deregister")

        headers = {}
        if self.token:
            headers["Authorization"] = self.token

        data = {"secret-key": self.secret, "correlation-id": self.correlation_id}
        data = json.dumps(data)
        url = f"https://{self.server}/deregister"
        try:
            async with ClientSession(None) as session:
                async with session.request("POST", url, data=data, headers=headers) as res:
                    if res:
                        text = await res.text()
                        if text and "success" in text:
                            return True
        except:
            pass
        log.error("Failed to de-register with interactsh server {self.server}")
        return False

    async def poll(self):
        if not self.server or not self.correlation_id or not self.secret:
            log.error(f"Missing required information to poll")

        headers = {}
        if self.token:
            headers["Authorization"] = self.token

        url = f"https://{self.server}/poll?id={self.correlation_id}&secret={self.secret}"

        ret = []
        try:
            async with ClientSession() as session:
                async with session.request("GET", url, headers=headers) as res:
                    if res:
                        text = await res.text()
                        if text:
                            text = json.loads(text)
                            data_list = text.get("data", None)
                            if data_list:
                                aes_key = text["aes_key"]
                                for data in data_list:
                                    decrypted_data = self.decrypt(aes_key, data)
                                    ret.append(decrypted_data)
        except:
            pass
        return ret

    def decrypt(self, aes_key, data):
        private_key = RSA.importKey(self.private_key)
        cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
        aes_plain_key = cipher.decrypt(base64.b64decode(aes_key))
        decode = base64.b64decode(data)
        bs = AES.block_size
        iv = decode[:bs]
        cryptor = AES.new(key=aes_plain_key, mode=AES.MODE_CFB, IV=iv, segment_size=128)
        plain_text = cryptor.decrypt(decode)
        return json.loads(plain_text[16:])