#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import sys
from bs4 import BeautifulSoup
from script import Script, SERVICE_PORT_MAP
type=sys.getfilesystemencoding()

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'web status'
        self.keyword = ['web', 'title', 'status']
        self.info = 'Get the web application status and title'
        self.type = 'info'
        self.level = 'info'
        Script.__init__(self, target=target, service_type=self.service_type)
        # super(POC, self).__init__(target=target,service_type=self.service_type)


    def prove(self):
        self.get_url()
        if self.url:
            codes = ['utf-8','gbk']
            status = str(0)
            title= ''
            result = self.curl('get', self.url)
            if result!=None:
                status = str(result.status_code)
                soup = BeautifulSoup(result.text, "html5lib")
                if soup!=None:
                    title = soup.title
                    if title == None or title.string == '':
                        title = "[None Title]".encode('utf-8')
                    else:
                        if result.encoding != None:
                            try:
                                title = title.string.encode(result.encoding)
                                codes.append(result.encoding)
                            except:
                                title = "[Error Code]".encode('utf-8')
                        else:
                            title = title.string
                    codes.append(type)
                    for j in range(0, len(codes)):
                        try:
                            title = title.decode(codes[j]).strip().replace("\r", "").replace("\n", "")
                            break
                        except:
                            continue
                        finally:
                            if j + 1 == len(codes):
                                title = '[Error Code]'
                else:
                    title = '[None Title]'

            if  status !='0':
                self.flag = 1
                self.res.append({"info": title , "key": status, "status": status})

if __name__=='__main__':
    print(POC('http://www.baidu.com').prove())