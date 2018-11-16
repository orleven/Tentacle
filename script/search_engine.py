#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

from random import choice

_Agents_list = ['Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
            ]

_Headers = {
                'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch, br',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Referer': 'https://www.baidu.com',
                'Cookie': '__jsluid=fae27ad046bd22fca181a42209bf2a21;',
                'User-Agent': choice(_Agents_list),
            }

_Proxy = {
    'http':'http://127.0.0.1:7999',
    'https':'http://127.0.0.1:7999'
    }

def get_script_info(data=None):
    script_info = {
        "name": "smtp Burst",
        "info": "This is a test.",
        "level": "low",
        "type": "info",
    }
    return script_info




def prove(data):
    search = 'powered by discuz'
    type1 = 'web'
    # type1 = 'host'
    page = 2
    # for z in _zoomeye(search, page, type1):
    #     for url in z:
    #         print(url)

    for url in _baidu(search,page):
        print(url)

    for url in _360so(search,page):
        print(url)

    for url in _bing(search, page):
        print(url)

    for url in _google(search, page):
        print(url)
    return data


# 钟馗之眼
def _zoomeye(search, page, z_type):
    """
        app:"Drupal" country:"JP"
    """
    import re
    import requests
    from bs4 import BeautifulSoup
    # url_login = "https://api.zoomeye.org/user/login"
    url_api = "https://www.zoomeye.org/api/search"

    # 认证信息
    Headers2 = {
        "Cube-Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IjI5OTY0Nzk4MjhAcXEuY29tIiwidXVpZCI6Ijk1YWQyZTY2NTk2MjlkNjMyMjZlZjI0MzUyMmQyNDA3IiwiaWF0IjoxNTIzOTQzNjM2LCJleHAiOjE1MjQwMzAwMzZ9.DdGIDsP4NnX_xkpm1IEmvnfYYmZqSl7V20Oc8axY3EE"}

    print("[!] Using zoomeye with type {0}\n".format(z_type) )

    for n in range(1, page + 1):
        try:
            data = {'q': search, 'p': str(n), 't': z_type}
            r = requests.get(url_api, params=data, headers=Headers2)

            if z_type == 'host':
                result = [str(item['ip']) + ':' + str(item['portinfo']['port']) for item in eval(r.content)['matches']]
            elif z_type == 'web':
                rer = re.compile('"url": "(.*?)"')
                result = rer.findall(r.content)
            yield result
        except Exception:
            yield None


# 百度搜索
def _baidu(search, page):
    import requests
    from urllib.parse  import quote
    from random import choice
    from bs4 import BeautifulSoup
    for n in range(0, page * 10, 10):
        base_url = 'https://www.baidu.com/s?wd=' + str(quote(search)) + '&oq=' + str(
            quote(search)) + '&ie=utf-8' + '&pn=' + str(n)
        try:
            r = requests.get(base_url, headers=_Headers)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('div.c-container > h3 > a'):
                url = requests.get(a['href'], headers=_Headers, timeout=5).url
                yield url
        except:
            yield None


# 360搜索
def _360so(search, page):
    import requests
    import re
    from urllib.parse  import quote
    from random import choice
    from bs4 import BeautifulSoup
    for n in range(1, page + 1):
        base_url = 'https://www.so.com/s?q=' + str(quote(search)) + '&pn=' + str(n) + '&fr=so.com'
        try:
            r = requests.get(base_url, headers=_Headers)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('li.res-list > h3 > a'):
                url1 = requests.get(a['href'], headers=_Headers, timeout=5)
                url = re.findall("URL='(.*?)'", url1.text)[0] if re.findall("URL='(.*?)'", url1.text) else url1.url
                yield url
        except:
            yield None


# 必应搜索
def _bing(search, page):
    import requests
    from urllib.parse  import quote
    from random import choice
    from bs4 import BeautifulSoup
    for n in range(1, (page * 10) + 1, 10):
        base_url = 'http://cn.bing.com/search?q=' + str(quote(search)) + '&first=' + str(n)
        try:
            r = requests.get(base_url, headers=_Headers)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('li.b_algo > div.b_algoheader > a'):
                url = a['href']
                yield url
        except:
            yield None


# Google搜索
def _google(search, page):
    import requests
    from urllib.parse  import quote
    from random import choice
    from bs4 import BeautifulSoup
    for n in range(0, 10 * page, 10):
        base_url = 'https://www.google.com.hk/search?safe=strict&q=' + str(quote(search)) + '&oq=' + str(
            quote(search)) + 'start=' + str(n)
        try:
            r = requests.get(base_url, headers={'User-Agent': choice(_Agents_list)}, proxies=_Proxy, timeout=16)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('div.rc > h3.r > a'):
                url = a['href']
                yield url
        except Exception as e:
            yield None



