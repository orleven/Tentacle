#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import requests
import chardet
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()


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
        try:
            result = requests.get(data['url'], headers=data['headers'], verify=False, timeout=data['timeout'])
            soup = BeautifulSoup(result.text, "html5lib")
            status = str(result.status_code)
            title = soup.title
            if title == None or title.string == '':
                title = "None Title".encode('utf-8')
            else:
                title = title.string.encode(result.encoding)
            code = chardet.detect(title)['encoding'] if chardet.detect(title)['encoding'] not in ['ISO-8859-5','KOI8-R','IBM855'] else 'gbk'
            # print(title.decode(code)+":"+code)
            title = title.decode(code).strip().replace("\r", "").replace("\n", "")
            data['flag'] = 1
            data['res'].append({"info": title, "key": title, "status": status})
        except :
            data['flag'] = 0
    return data

