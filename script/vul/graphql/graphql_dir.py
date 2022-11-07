#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    Graphql
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.name = 'GraphqlDir'
        self.service_type = ServicePortMap.WEB
        self.dir_list = [
            "",
            'server/',
            'api/',
        ]
        self.file_dic = {
            'graphql?query={__schema{types{name fields{name args{name}type{name}}}}}': "\"__schema\"",
            'g?query={__schema{types{name fields{name args{name}type{name}}}}}': "\"__schema\"",
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