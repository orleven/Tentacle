#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

_file_dic = {
    "overview": None,
    "state.json": None,
    "mappings.json": None,
    "consul": None,
    "trace": None,
    "swagger-ui.html": None,
    "swagger.json": None,
    "metrics": None,
    "info": None,
    "env": None,
    "heapdump": None,
    "loggers": None,
    "hystrix.stream": None,
    "auditevents": None,
    "httptrace": None,
    "features": None,
    "api-docs/": None,
    "v1/api-docs": None,
    "v2/api-docs": None,
    "docs/": 'swagger-ui',
    "swagger/swagger-ui.html": None,
    "actuator/trace": None,
    "actuator/heapdump": None,
    "actuator/metrics": None,
    "actuator/info": None,
    "actuator/env": None,
    "actuator/loggers": None,
    "actuator/hystrix.stream": None,
    "actuator/auditevents": None,
    "actuator/httptrace": None,

    "api/swagger-ui.html": None,
    "api/web/swagger-ui.html": None,
    "api/actuator/trace": None,
    "api/actuator/heapdump": None,
    "api/actuator/metrics": None,
    "api/actuator/info": None,
    "api/actuator/env": None,
    "api/actuator/loggers": None,
    "api/actuator/hystrix.stream": None,
    "api/actuator/auditevents": None,
    "api/actuator/httptrace": None,
}

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'spring info'
        self.keyword = ['web']
        self.info = 'spring info'
        self.type = VUL_TYPE.INFO
        self.level = VUL_LEVEL.LOWER
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                path_list = list(set([
                    self.url_normpath(self.base_url, '/'),
                    self.url_normpath(self.url, './'),
                    self.url_normpath(self.url, '../'),
                ]))
                for path in path_list:
                    # 404 page
                    # Replace the main factors affecting 404 pages to reduce false positives
                    length1 = length2 = 0
                    fix_length = 10
                    # min_length = 10240
                    async with session.get(url=path + 'is_not_exist', allow_redirects=False) as res1:
                        length1 = len((await res1.text()).replace('is_not_exist', '')) if res1 else 0
                    async with session.get(url=path + '.is_not_exist', allow_redirects=False) as res1:
                        length2 = len((await res1.text()).replace('.is_not_exist', '')) if res1 else 0

                    # fix bug, file too large would timeout
                    # read_length = (length1 + length2) * 2 + min_length

                    # burst page:
                    for key in _file_dic.keys():
                        url = path + key
                        async with session.get(url=url, allow_redirects=False) as response:
                            if response != None:
                                if response.status == 200:
                                    # Replace the main factors affecting 404 pages to reduce false positives
                                    text = await response.text()
                                    text = text.replace(key, '')
                                    # text = await response.content.read(read_length)

                                    if _file_dic[key] == None:
                                        length = len(text)
                                        if abs(length - length1) > fix_length and abs(length - length2) > fix_length:
                                            self.flag = 1
                                            self.res.append({"info": url, "key": 'spring info file'})
                                    else:
                                        text = str(text)
                                        if _file_dic[key] in text.lower():
                                            self.flag = 1
                                            self.res.append({"info": url, "key": 'spring info file'})
