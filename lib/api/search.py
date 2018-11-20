#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import requests
import re
import json
import sys
from urllib.parse import quote
from random import choice
from bs4 import BeautifulSoup
from lib.core.settings import HEADERS
from lib.core.settings import AGENTS_LIST
# from lib.core.settings import ZOOMEYS_API
from lib.core.data import logger
from lib.core.data import conf

_Proxy = {
    'http':'http://127.0.0.1:7999',
    'https':'http://127.0.0.1:7999'
    }

def search_api(search,page = 5):
    target_list = []
    if 'target_zoomeye' in conf.keys():
        for type in ['host','web']:
            for z in _zoomeye_api(search, page, type):
                for url in z:
                    target_list.append(url)

    elif 'target_github' in conf.keys():
        for z in _github_api(search, page):
            print(z)
    return list(set(target_list))

def search_engine(search,page = 5):
    target_list = []
    try:
        for url in _baidu(search,page):
            target_list.append(url)

        for url in _360so(search,page):
            target_list.append(url)

        for url in _bing(search, page):
            target_list.append(url)

        for url in _google(search, page):
            target_list.append(url)
    except KeyboardInterrupt:
        sys.exit(logger.error("Exit by user."))

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
            for a in soup.select('div.rc > div.r > a'):
                url = a['href']
                if 'translate.google.com' not in url:
                    yield url
        except Exception as e:
            yield None


def _zoomeye_api(search, page, z_type):
    """
        app:"Drupal" country:"JP"
        curl -X POST https://api.zoomeye.org/user/login -d '
        {
        "username": "username@qq.com",
        "password": "password"
        }'
    """
    headers = HEADERS
    url_login = 'https://api.zoomeye.org/user/login'
    try:
        data = {
            'username': conf['config']['zoomeye_api']['username'],
            'password': conf['config']['zoomeye_api']['password']
        }
        res = requests.post(url_login, json=data, headers=headers)
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: zoomeye_api, please check the config in tentacle.conf."))
    headers["Authorization"] = "JWT " + json.loads(res.text)['access_token']

    if z_type.lower() == 'web':
        url_api = "https://api.zoomeye.org/web/search"
    elif z_type.lower() == 'host':
        url_api = "https://api.zoomeye.org/host/search"
    else:
        logger.error("Error Zoomeye api with type {0}.".format(z_type))
        return None
    logger.sysinfo("Using Zoomeye api with type {0}.".format(z_type))
    for n in range(1, page + 1):
        try:
            data = {'query': search, 'page': str(n)}
            res = requests.get(url_api, params=data, headers=headers)
            if int(res.status_code) == 422:
                sys.exit(logger.error("Error Zoomeye api token."))
            if z_type.lower() == 'web':
                result = re.compile('"url": "(.*?)"').findall(res.text)
            elif z_type.lower() == 'host':
                result = [str(item['ip']) + ':' + str(item['portinfo']['port']) for item in json.loads(res.text)['matches']]

            yield result
        except Exception:
            yield None



def _github_api(search, page):
    '''
        https://github.com/settings/tokens
        Generate new token
    '''
    per_page_limit = 50
    github_timeout = 20  #

    InformationRegex = {"mail": r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
                        "domain": r"(http[s]*://[^<|\"|?]*)",
                        "pass1": r"(pass[^<|?]{30})",
                        "pass2": r"(password[^<|?]{30})",
                        "pass3": r"(pwd[^<|?]{30})",
                        "root": r"(root[^<|?]{0,30})",
                        "title": r"<title>(.*)<\/title>",
                        "ip": r"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:*[0-9]{0,5})"}

    headers = HEADERS
    url_api = "https://api.github.com/search/code?sort=updated&order=desc&per_page=%s&q=" %per_page_limit
    try:
        token = conf['config']['github_api']['token']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: github_api, please check the config in tentacle.conf."))
    headers["Authorization"] = "token " + token
    try:
        resp = requests.get(url_api + search, headers=headers, timeout=github_timeout)
    except:
        resp = None
    if resp and resp.status_code == 200:
        logger.sysinfo("Using github api...")
        res_json = json.loads(resp.content)
        total = res_json["total_count"]
        logger.sysinfo("Found github url: %d"%int(total))
        page_num = (total // per_page_limit) + 1

        for p in range(page_num):
            # Search url
            git_urls = []
            _url_api = "https://api.github.com/search/code?sort=updated&order=desc&page=%d&per_page=%s&q=" % (p,per_page_limit)
            try:
                _resp = requests.get(_url_api + search, headers=headers, timeout=github_timeout)
            except:
                _resp = None
            if _resp and _resp.status_code == 200:
                logger.sysinfo("Found github url of %d page..." % int(p))
                try:
                    _res_json = json.loads(_resp.content)
                    for i in range(len(_res_json['items'])):
                        git_urls.append(_res_json['items'][i]["html_url"])
                except:
                    pass

                # Access url and match
                git_urls = list(set(git_urls))
                for url in git_urls:
                    try:
                        _resp = requests.get(url, timeout=github_timeout)
                    except:
                        _resp = None
                    if _resp and _resp.status_code == 200:

                        for i in InformationRegex:
                            # try:
                            _text = _resp.text.lower()
                            _text = _text.replace('&quot;', '"')
                            _text = _text.replace('&amp;', '&')
                            _text = _text.replace('&lt;', '<')
                            _text = _text.replace('&gt;', '>')
                            _text = _text.replace('&nbsp;', ' ')

                            res = re.findall(InformationRegex[i], _text)
                            for _re in res:
                                if 'github' not in _re:
                                    if search in _re:
                                        if InformationRegex[i] == 'mail' :
                                            logger.sysinfo("Found info: %s [%s]"%(url,_re))
                                        elif InformationRegex[i] == 'domain' :
                                            logger.sysinfo("Found info: %s [%s]" % (url, _re))
                                        elif 'pass' in InformationRegex[i]:
                                            logger.sysinfo("Found info: %s [%s]" % (url, _re))


            elif int(_resp.status_code) == 422:
                sys.exit(logger.error("Error github api token."))
    elif int(resp.status_code) == 422:
        sys.exit(logger.error("Error github api token."))
    return []