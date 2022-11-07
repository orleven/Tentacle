#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import re
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB
        self.file_list = ["admin.bz2", "admin.gz", "admin.log", "admin.sql", "admin.tar", "admin.tar.bz2", "admin.tar.gz", "admin.tgz", "admin.zip", "backup.bz2", "backup.gz", "backup.sql", "backup.tar", "backup.tar.bz2", "backup.tar.gz", "backup.tgz", "backup.zip", "data.7z", "data.bz", "data.log", "data.sql", "data.tar.gz", "data.zip", "database.bz2", "database.gz", "database.sql", "database.tar", "database.tar.bz2", "database.tar.gz", "database.tgz", "database.zip", "db.bz2", "db.gz", "db.sql", "db.tar", "db.tar.bz2", "db.tar.gz", "db.tgz", "db.zip", "web.bz2", "web.gz", "web.log", "web.sql", "web.tar", "web.tar.bz2", "web.tar.gz", "web.tgz", "web.zip", "webroot.bz2", "webroot.gz", "webroot.sql", "webroot.tar", "webroot.tar.bz2", "webroot.tar.gz", "webroot.tgz", "webroot.zip", "www.bz2", "www.gz", "www.sql", "www.tar", "www.tar.bz2", "www.tar.gz", "www.tgz", "www.zip"]

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        for file_name in self.file_list:
                            url = path + file_name

                            try:
                                async with session.get(url=url, allow_redirects=False) as res:
                                    if res and res.status == 200 and res.headers.get("Content-Type", "text/html") == "application/octet-stream" and res.content_length > 1024 * 1024 * 4:
                                        yield url

                            except:
                                pass
