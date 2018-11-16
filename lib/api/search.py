#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import requests
import re
from urllib.parse import quote
from random import choice
from bs4 import BeautifulSoup
from lib.core.settings import HEADERS
from lib.core.settings import AGENTS_LIST
from lib.core.data import logger

_Proxy = {
    'http':'http://127.0.0.1:7999',
    'https':'http://127.0.0.1:7999'
    }

def search_engine(search,page = 2):
    target_list = []
    # search = 'powered by discuz'
    # type1 = 'web'
    # type1 = 'host'
    # for z in _zoomeye(search, page, type1):
    #     for url in z:
    #         print(url)

    for url in _baidu(search,page):
        target_list.append(url)

    for url in _360so(search,page):
        target_list.append(url)

    for url in _bing(search, page):
        target_list.append(url)

    for url in _google(search, page):
        target_list.append(url)

    return list(set(target_list))



def _baidu(search, page):
    for n in range(0, page * 10, 10):
        base_url = 'https://www.baidu.com/s?wd=' + str(quote(search)) + '&oq=' + str(
            quote(search)) + '&ie=utf-8' + '&pn=' + str(n)
        try:
            r = requests.get(base_url, headers=HEADERS)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('div.c-container > h3 > a'):
                url = requests.get(a['href'], headers=HEADERS, timeout=5).url
                yield url
        except:
            yield None


# 360搜索
def _360so(search, page):
    for n in range(1, page + 1):
        base_url = 'https://www.so.com/s?q=' + str(quote(search)) + '&pn=' + str(n) + '&fr=so.com'
        try:
            r = requests.get(base_url, headers=HEADERS)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('li.res-list > h3 > a'):
                url1 = requests.get(a['href'], headers=HEADERS, timeout=5)
                url = re.findall("URL='(.*?)'", url1.text)[0] if re.findall("URL='(.*?)'", url1.text) else url1.url
                yield url
        except:
            yield None


# 必应搜索
def _bing(search, page):
    for n in range(1, (page * 10) + 1, 10):
        base_url = 'http://cn.bing.com/search?q=' + str(quote(search)) + '&first=' + str(n)
        try:
            r = requests.get(base_url, headers=HEADERS)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('li.b_algo > div.b_algoheader > a'):
                url = a['href']
                yield url
        except:
            yield None


# Google搜索
def _google(search, page):
    for n in range(0, 10 * page, 10):
        base_url = 'https://www.google.com.hk/search?safe=strict&q=' + str(quote(search)) + '&oq=' + str(
            quote(search)) + 'start=' + str(n)
        try:
            r = requests.get(base_url, headers={'User-Agent': choice(AGENTS_LIST)}, proxies=_Proxy, timeout=16)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('div.rc > h3.r > a'):
                url = a['href']
                yield url
        except Exception as e:
            yield None

# 钟馗之眼
def _zoomeye(search, page, z_type):
    """
        app:"Drupal" country:"JP"
    """
    # url_login = "https://api.zoomeye.org/user/login"
    url_api = "https://www.zoomeye.org/api/search"

    # 认证信息
    header = HEADERS
    header["Cube-Authorization"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IjI5OTY0Nzk4MjhAcXEuY29tIiwidXVpZCI6Ijk1YWQyZTY2NTk2MjlkNjMyMjZlZjI0MzUyMmQyNDA3IiwiaWF0IjoxNTIzOTQzNjM2LCJleHAiOjE1MjQwMzAwMzZ9.DdGIDsP4NnX_xkpm1IEmvnfYYmZqSl7V20Oc8axY3EE"
    logger.warning("Using zoomeye with type {0}".format(z_type) )

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


