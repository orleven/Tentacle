#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import chardet
from bs4 import BeautifulSoup
import sys
type=sys.getfilesystemencoding()

def info(data=None):
    info = {
        "name": "web content",
        "info": "web content.",
        "level": "low",
        "type": "info",
    }
    return info

def prove(data):
    data = init(data,'web')
    if data['url']:
        webkeydic = _read_dic(data['dic_one']) if 'dic_one' in data.keys() else  _read_dic('dict/web_content_key.txt')
        codes = ['utf-8', 'gbk']
        try:
            result = curl('get',data['url'])
        except:
            return data

        content = result.text
        soup = BeautifulSoup(content, "html5lib")
        status = result.status_code
        try:
            title = soup.title.string
            title = title.encode(result.encoding)
        except:
            title = "[None Title]".encode('utf-8')

        try:
            codes.append(type)
            codes.append(result.encoding)
            content = content.encode(result.encoding) if content != None else ''.encode('utf-8')
        except:
            pass

        for j in range(0, len(codes)):
            try:
                title = title.decode(codes[j]).strip().replace("\r", "").replace("\n", "")
                break
            except:
                pass
            finally:
                if j + 1 == len(codes):
                    content = ''
                    title = '[Error Code]'

        key = ''
        for searchkey in webkeydic:
            searchkey = str(searchkey,'utf-8').replace("\r", "").replace("\n", "")
            try:

                if searchkey  in title or searchkey in content.encode(result.encoding):
                    key += searchkey + ','
                    data['flag'] = 1
            except:
                pass

        if data['flag'] == 1:
            data['res'].append({"info": title, "key": key[:-1], "status": status})

    return data



def _read_dic(dicname):
    with open(dicname, 'rb') as f:
        return f.readlines()