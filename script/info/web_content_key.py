#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

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
        result = curl('get', data['url'])
        if result != None:
            status = result.status_code

            # Text
            webkeydic = _read_dic(data['dic_one']) if 'dic_one' in data.keys() else  _read_dic('dict/web_content_key.txt')
            content = result.text
            key = ''
            for searchkey in webkeydic:
                searchkey = str(searchkey, 'utf-8').replace("\r", "").replace("\n", "")
                try:
                    if searchkey in content:
                        key += searchkey + ','
                        data['flag'] = 1
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

            if data['flag'] == 1:
                data['res'].append({"info": title, "key": key[:-1], "status": status})

    return data



def _read_dic(dicname):
    with open(dicname, 'rb') as f:
        return f.readlines()