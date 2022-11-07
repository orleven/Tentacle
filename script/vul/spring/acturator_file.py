#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    ActuratorFile
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

        self.dir_list = [
            "",
            "api/",
            "actuator/",
            ";/actuator/",
            "api/actuator/",
            "api/;/actuator/",
            "v2/",
            "v1/",
            "web/",
            "swagger/",
            "gateway/actuator/",
            # "%61%63%74%75%61%74%6f%72/",  # aiohttp 目前版本户会自动解码url编码
        ]
        self.file_dic = {
            "consul": "Services",
            "swagger-ui.html": 'swaggerui',
            "swagger.json": "\"swagger\"",
            "metrics": "\"names\"",
            "info": "\"names\"",
            "env": "spring",
            "routes": "\"route_",
            "mappings": "springframework",
            "loggers": "\"loggers\"",
            "hystrix.stream": "Hystrix",
            "auditevents": "\"events\"",
            "httptrace": "\"headers\":{",
            "features": "springframework",
            "caches": "cachemanagers",
            "beans": "springframework",
            "conditions": "springframework",
            "configprops": "spring",
            "threaddump": "springframework",
            "scheduledtasks": "cron",
            "api-docs": "\"swagger\"",
            "mappings.json": "bean:",
            "trace": "\"headers\":{",
            "dump": "threadName",
            "gateway/routes": "cloud.gateway.",
            "gateway/globalfilters": "cloud.gateway.filter",
            "gateway/routefilters": "GatewayFilter",
        }

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        for dir_path in self.dir_list:
                            for file_path, file_keyword in self.file_dic.items():
                                try:
                                    url = path + dir_path + file_path
                                    async with session.get(url=url, allow_redirects=False) as res:
                                        if res and res.status == 200:
                                            text_source = await res.text()
                                            text = text_source.lower()
                                            if text and file_keyword.lower() in text.lower():
                                                yield url
                                except:
                                    pass

                            try:
                                url = path + dir_path + "heapdump"
                                async with session.head(url=url, allow_redirects=False) as res:
                                    if res and res.status == 200:
                                        if res.headers.get("Content-Type", "text/html") == "application/octet-stream" and res.content_length > 1024 * 1024 * 4:
                                            yield url
                            except:
                                pass