#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

def info(data=None):
    info = {
        "name": "info file",
        "info": "info file.",
        "level": "low",
        "type": "info"
    }
    return info

_file_dic = {
    "crossdomain.xml": 'allow-access-from domain="*"',
    ".svn/entries": None,
    ".svn/wc.db": None,
    "WEB-INF/web.xml": "<web-app",
    "robots.txt": None,
    ".git": None,
    ".git/HEAD": None,
    ".git/index": None,
    ".git/config": None,
    ".git/description": None,
    "README.MD": None,
    "README.md": None,
    "README": None,
    ".DS_store": None,
    "WEB-INF/database.propertie": None,
    ".htaccess": None,
    "phpinfo.php": None,
    "test.php":None,
}

def prove(data):
    data = init(data,'web')
    if data['base_url']:
        flag = 3
        for key in _file_dic.keys():
            if flag == 0 :
                break
            url = data['base_url'] + key
            res = curl('get', url,allow_redirects=False)
            if res != None:
                if res.status_code == 200 :
                    if _file_dic[key] == None or _file_dic[key] in res.text.lower():
                        data['flag'] = 1
                        data['res'].append({"info": url, "key": key})
            else:
                flag -= 1
    return data
