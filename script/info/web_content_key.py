#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import requests
import chardet
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

def get_script_info(data=None):
    script_info = {
        "name": "web content",
        "info": "web content.",
        "level": "low",
        "type": "info",
    }
    return script_info

def prove(data):
    data = init(data,'web')
    if data['url']:
        webkeydic = _read_dic(data['dic_one']) if 'dic_one' in data.keys() else  _read_dic('dict/web_content_key.txt')
        try:
            result = requests.get(data['url'], headers=data['headers'], verify=False, timeout=data['timeout'])
            status = str(result.status_code)
            content = result.text
            key = ''
            if result.encoding != None:
                encoding = result.encoding
                try:
                    content = str(content).encode(encoding).decode('utf-8')
                except:
                    # content = content.encode(encoding).decode('gbk') #  58.216.167.66 IBM855
                    # content = content # 163 GBK
                    # content = str(content).encode(encoding).decode('utf-8') # 百度  ISO-8859-1
                    pass
            else:
                encoding = 'None Encoding'
                # code = chardet.detect(title)['encoding'] if chardet.detect(title)['encoding'] not in ['ISO-8859-5','KOI8-R'] else 'gbk'
                # print(title.decode(code)+":"+code)
            for searchkey in webkeydic:
                _key = searchkey.strip('\n').strip('\r').strip()
                if _key.lower() in str(content).lower():
                    key += _key + ','
                    data['flag'] = 1

            soup = BeautifulSoup(content, "html5lib")
            title = soup.title.string if soup.title != None else "None Title"
            title = title.strip().replace("\r", "").replace("\n", "")
            if data['flag']:
                data['res'].append({"info": title, "key": key[:-1], "status": status, "encoding": encoding})
        except:
            pass
    return data



def _read_dic(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()