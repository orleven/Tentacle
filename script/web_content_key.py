#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'



def get_script_info(data=None):
    script_info = {
        "name": "web content",
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
    if 'cookie' in data.keys() != "":
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
    webkeydic = _read_dic(data['dic_one']) if 'dic_one' in data.keys() else  _read_dic('dict/web_content_key.txt')
    try:
        import chardet
        from bs4 import BeautifulSoup
        result = requests.get(url, headers=headers, verify=False, timeout=5)
        status = str(result.status_code)
        content = result.text

        key = ''
        if result.encoding != None:
            encoding = result.encoding
            try:
                content = str(content).encode(encoding).decode('utf-8')

            except:
                # content = content.encode(encoding).decode('gbk') #  58.216.167.66 IBM855
                # content = content # 163 GBK
                # content = str(content).encode(encoding).decode('utf-8') # 百度  ISO-8859-1
                pass
        else:
            encoding = 'None Encoding'
            # code = chardet.detect(title)['encoding'] if chardet.detect(title)['encoding'] not in ['ISO-8859-5','KOI8-R'] else 'gbk'
            # print(title.decode(code)+":"+code)

        for searchkey in webkeydic:
            _key = searchkey.strip('\n').strip('\r').strip()
            if  _key.lower() in str(content).lower():
                key += _key + ','
                data['flag'] = True

        soup = BeautifulSoup(content, "html5lib")
        title = soup.title.string if soup.title!=None else "None Title"
        title = title.strip().replace("\r", "").replace("\n", "")

        if data['flag']:
            data['res'].append({"info":  title,"key":key[:-1],"status":status,"encoding":encoding})
            data['url'] = url
    except :
        return False
    return True

def _read_dic(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()