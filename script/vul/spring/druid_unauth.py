#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from script import BaseScript
from lib.core.enums import ServicePortMap
from lib.util.aiohttputil import ClientSession

class Script(BaseScript):
    """
    Druid未授权访问
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB
        self.dir_list = [
            "",
            'druid/',
            'server/druid/',
            'api/druid/',
            'app/druid/',
            'api/app/druid/',
        ]
        self.file_list = [
            'console.html',
            'sql.html',
            'index.html',
        ]

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        for dir_path in self.dir_list:
                            for file_path in self.file_list:
                                try:
                                    url = path + dir_path + file_path
                                    async with session.get(url=url, allow_redirects=False) as res:
                                        if res and res.status == 200:
                                            text_source = await res.text()
                                            text = text_source.lower()
                                            if 'druid stat index' in text or "druid version" in text or 'druid indexer' in text or 'druid sql stat' in text or 'druid monitor' in text:
                                                yield url
                                except:
                                    pass
