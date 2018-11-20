#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import sys
import requests
import chardet
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()
type=sys.getfilesystemencoding()

def get_script_info(data=None):
    script_info = {
        "name": "web status",
        "info": "Web status.",
        "level": "low",
        "type": "info",
    }
    return script_info

def prove(data):
    data = init(data, 'web')
    if data['url']:
        codes = ['utf-8','gbk']
        status = str(0)
        title= ''
        try:
            result = requests.get(data['url'], headers=data['headers'], verify=False, timeout=data['timeout'])
            soup = BeautifulSoup(result.text, "html5lib")
            status = str(result.status_code)
            title = soup.title
            if title == None or title.string == '':
                title = "[None Title]".encode('utf-8')
            else:
                title = title.string.encode(result.encoding)
            # code = chardet.detect(title)['encoding'] if chardet.detect(title)['encoding'] not in ['windows-1255','GB2312','ISO-8859-5','ISO-8859-9','KOI8-R','IBM855'] else 'gbk'

            # if chardet.detect(title)['encoding'] in ['windows-1255','GB2312','ISO-8859-5','ISO-8859-9','KOI8-R','IBM855']:
            #     code = 'gbk'
            # else:
            #     code = chardet.detect(title)['encoding']
            # title = title.decode(code).strip().replace("\r", "").replace("\n", "")

            codes.append(result.encoding)
            codes.append(type)
            for j in range(0, len(codes)):
                try:
                    title = title.decode(codes[j]).strip().replace("\r", "").replace("\n", "")
                    break
                except:
                    pass
                finally:
                    if j + 1 == len(codes):
                        title = '[Error Code]'
        except:
            pass
        if  status !='0':
            data['flag'] = 1
            data['res'].append({"info": title , "key": status, "status": status})
    return data

