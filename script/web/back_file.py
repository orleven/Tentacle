#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

_file_dic = {
    "access.log": None,
    "admin.bz2": None,
    "admin.gz": None,
    "admin.log": None,
    "admin.sql": None,
    "admin.tar": None,
    "admin.tar.bz2": None,
    "admin.tar.gz": None,
    "admin.tgz": None,
    "admin.zip": None,
    "backup.bz2": None,
    "backup.gz": None,
    "backup.sql": None,
    "backup.tar": None,
    "backup.tar.bz2": None,
    "backup.tar.gz": None,
    "backup.tgz": None,
    "backup.zip": None,
    "data.7z": None,
    "data.bz": None,
    "data.log": None,
    "data.sql": None,
    "data.tar.gz": None,
    "data.zip": None,
    "database.bz2": None,
    "database.gz": None,
    "database.sql": None,
    "database.tar": None,
    "database.tar.bz2": None,
    "database.tar.gz": None,
    "database.tgz": None,
    "database.zip": None,
    "db.bz2": None,
    "db.gz": None,
    "db.sql": None,
    "db.tar": None,
    "db.tar.bz2": None,
    "db.tar.gz": None,
    "db.tgz": None,
    "db.zip": None,
    "error.log": None,
    "password": None,
    "password.txt": None,
    "username": None,
    "username.txt": None,
    "web.bz2": None,
    "web.gz": None,
    "web.log": None,
    "web.sql": None,
    "web.tar": None,
    "web.tar.bz2": None,
    "web.tar.gz": None,
    "web.tgz": None,
    "web.zip": None,
    "webroot.bz2": None,
    "webroot.gz": None,
    "webroot.sql": None,
    "webroot.tar": None,
    "webroot.tar.bz2": None,
    "webroot.tar.gz": None,
    "webroot.tgz": None,
    "webroot.zip": None,
    "www.bz2": None,
    "www.gz": None,
    "www.sql": None,
    "www.tar": None,
    "www.tar.bz2": None,
    "www.tar.gz": None,
    "www.tgz": None,
    "www.zip": None,
}

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'back file'
        self.keyword = ['web']
        self.info = 'back file'
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
                    fix_length = 50
                    # min_length = 10240
                    async with session.get(url=path+'is_not_exist', allow_redirects=False) as res1:
                        length1 = len((await res1.text()).replace('is_not_exist', '')) if res1 else 0
                    async with session.get(url=path + '.is_not_exist', allow_redirects=False) as res1:
                        length2 = len((await res1.text()).replace('.is_not_exist', '')) if res1 else 0

                    # fix bug, file too large would timeout
                    # read_length = (length1 + length2) * 2 + min_length

                    # burst page:
                    for key in _file_dic.keys():
                        url = path + key
                        try:
                            async with session.get(url=url, allow_redirects=False) as response:
                                if response != None:
                                    if response.status == 200:
                                        # Replace the main factors affecting 404 pages to reduce false positives
                                        text = await response.text()
                                        text = text.replace(key, '')
                                        # text = await response.content.read(read_length)

                                        if _file_dic[key] == None:
                                            length = len(text)
                                            if abs(length-length1) > fix_length and abs(length-length2) > fix_length:
                                                self.flag = 1
                                                self.res.append({"info": url, "key": 'back file'})
                                        else:
                                            text = str(text)
                                            if _file_dic[key] in text.lower():
                                                self.flag = 1
                                                self.res.append({"info": url, "key": 'back file'})
                        except:
                            pass
