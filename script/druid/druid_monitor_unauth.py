1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script, VUL_TYPE, VUL_LEVEL

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'druid-monitor-unauth'
        self.keyword = ['web', 'druid']
        self.info = 'druid-monitor-unauth'
        self.type = VUL_TYPE.UNAUTH
        self.level = VUL_LEVEL.HIGH
        self.repair = ''
        self.refer = ''
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        await self.get_url()
        if self.base_url != None:
            async with ClientSession() as session:
                file_list = ['console.html', 'sql.html', 'index.html']
                for path in self.url_normpath(self.url, [
                    './',
                    './druid/',
                    './server/druid/',
                    './api/druid/',
                    './app/druid/',
                    './api/app/druid/',
                    './api/saas/apisvr/druid/',
                ]):
                    for file in file_list:
                        url = path+file
                        async with session.get(url=path+file, allow_redirects=False) as res:
                            if res and res.status == 200:
                                text = await res.text()
                                text = text.lower()
                                if 'druid stat index' in text or "druid version" in text or 'druid indexer' in text or 'druid sql stat' in text or 'druid monitor' in text:
                                    self.flag = 1
                                    self.res.append({"info": url, "key": "druid-monitor-unauth"})
                                    return