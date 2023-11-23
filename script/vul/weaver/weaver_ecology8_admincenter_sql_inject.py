#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    """
    ecology8 admincenter sql inject
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        url = path +"admincenter/interfaces/interfaceCheckExists.jsp?className="
                        async with session.get(url=url) as res:
                            if res!=None:
                                text = await res.text()
                                if 'false' == text.replace('\r','').replace('\n','').replace(' ',''):
                                    yield url
                   