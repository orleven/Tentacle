#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from bs4 import BeautifulSoup
import sys
type=sys.getfilesystemencoding()
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'web content key'
        self.keyword = ['web', 'title', 'keyword']
        self.info = 'Get the web application status and search keyword'
        self.type = 'info'
        self.level = 'info'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.url:
            result = self.curl('get', self.url)
            if result != None:
                status = result.status_code

                webkeydic = self.read_file(self.parameter['keyword'], 'rb') if 'keyword' in self.parameter.keys() else self.read_file('dict/web_content_key.txt', 'rb')
                content = result.text
                key = ''
                for searchkey in webkeydic:
                    searchkey = str(searchkey, 'utf-8').replace("\r", "").replace("\n", "")
                    try:
                        if searchkey in content:
                            key += searchkey + ','
                            self.flag = 1
                    except Exception as e:
                        print(e)
                        pass

                # title
                soup = BeautifulSoup(result.text, "html5lib")
                if soup != None:
                    codes = ['utf-8', 'gbk']
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

                if self.flag == 1:
                    self.res.append({"info": title, "key": key[:-1], "status": status})
