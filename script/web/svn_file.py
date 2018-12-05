#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

def info(data=None):
    info = {
        "name": "svn file",
        "info": "svn file.",
        "level": "medium",
        "type": "info"
    }
    return info

def prove(data):
    data = init(data,'web')
    if data['base_url']:
        url = data['base_url']+'.svn/entries'
        try:
            res =curl('get',url)
            if "dir" in res.text or "file" in res.text and res.status_code == 200:
                data['flag'] = 1
                data['data'].append({"page": '/.svn/entries'})
                data['res'].append({"info": url, "key": "/.svn/entries"})
        except:
            pass
    return data
