#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import sys
from bs4 import BeautifulSoup
type=sys.getfilesystemencoding()

def info(data=None):
    info = {
        "name": "web status",
        "info": "Web status.",
        "level": "low",
        "type": "info",
    }
    return info

def prove(data):
    data = init(data, 'web')
    if data['url']:
        codes = ['utf-8','gbk']
        status = str(0)
        title= ''
        result = curl('get',data['url'])
        if result!=None:
            status = str(result.status_code)

            soup = BeautifulSoup(result.text, "html5lib")
            if soup!=None:
                title = soup.title
                if title == None or title.string == '':
                    title = "[None Title]".encode('utf-8')
                else:
                    if result.encoding != None:
                        title = title.string.encode(result.encoding)
                        codes.append(result.encoding)
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
            data['flag'] = 1
            data['res'].append({"info": title , "key": status, "status": status})
    return data

