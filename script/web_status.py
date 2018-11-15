#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'



def get_script_info(data=None):
    script_info = {
        "name": "web status",
        "info": "This is a test.",
        "level": "low",
        "type": "info",
        "author": "orleven",
        "url": "",
        "keyword": "tag:iis",
        "source": 1
    }
    return script_info

def prove(data):
    '''
    data = {
        "target_host":"",
        "target_port":"",
        "proxy":"",
        "dic_one":"",
        "dic_two":"",
        "cookie":"",
        "url":"",
        "flag":"",
        "data":"",
        "":"",

    }

    '''


    headers = {}
    if 'cookie' in data.keys():
        headers["Cookie"] = data['cookie']
    headers[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    if 'url' in data.keys() and data['url']!=None:
        _curl(data,data['url'] ,headers)
    else:

        if data['target_port'] == 0:
            target = data['target_host']
        else:
            target = data['target_host'] + ":" + str(data['target_port'])
        for pro in ['http://', "https://"]:

            if _curl(data,pro + target , headers):
                if pro == 'http://':
                    data['target_port'] = 80
                else:
                    data['target_port'] = 443
                return data
    return data


def _curl(data,url,headers):

    import requests
    requests.packages.urllib3.disable_warnings()
    import  threading
    try:
        import sys
        import chardet
        from bs4 import BeautifulSoup
        result = requests.get(url , headers=headers, verify=False, timeout=5)
        soup = BeautifulSoup(result.text, "html5lib")
        status = str(result.status_code)
        title = soup.title

        if title == None or title.string == '':
            title = "None Title".encode('utf-8')
        else:
            title = title.string.encode(result.encoding)
        # 打印   编码控制
        code = chardet.detect(title)['encoding'] if chardet.detect(title)['encoding'] not in ['ISO-8859-5','KOI8-R','IBM855'] else 'gbk'
        # print(title.decode(code)+":"+code)

        title = title.decode(code).strip().replace("\r","").replace("\n","")
        data['flag'] = True
        data['res'].append({"info": title,"key":title,"status":status})
        data['url'] = url
    except :
        return False
    return True
