#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re
import json
import time
import sys
import shodan
from bs4 import BeautifulSoup
from urllib.parse import quote
from lib.utils.cipher import base64encode
from lib.utils.curl import mycurl
from lib.core.data import logger
from lib.core.data import conf
from lib.utils.utils import random_string

def search_api(search,page = 50):
    target_list = []
    try:
        if 'target_zoomeye' in conf.keys():
            for type in ['host','web']:
                for z in _zoomeye_api(search, page, type):
                    for url in z:
                        target_list.append(url)

        elif 'target_shodan' in conf.keys():
            for z in _shodan_api(search, page):
                target_list.append(z)

        elif 'target_fofa' in conf.keys():
            for z in _fofa_api(search, page):
                target_list.append(z)

        elif 'target_fofa_today_poc' in conf.keys():
            for z in _fofa_api_today_poc(page):
                target_list.append(z)

        elif 'target_github' in conf.keys():
            for z in _github_api(search, page):
                target_list.append(z)

        elif 'target_google' in conf.keys():
            for z in _google_api(search, page):
                target_list.append(z)

    except KeyboardInterrupt:
        sys.exit(logger.error("Exit by user."))

    if isinstance(target_list,tuple):
        return target_list
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
    except KeyboardInterrupt:
        sys.exit(logger.error("Exit by user."))

    return list(set(target_list))

def _baidu(search, page):
    for n in range(0, page * 10, 10):
        base_url = 'https://www.baidu.com/s?wd=' + str(quote(search)) + '&oq=' + str(
            quote(search)) + '&ie=utf-8' + '&pn=' + str(n)
        try:
            r = mycurl('get',base_url)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('div.c-container > h3 > a'):
                url = mycurl('get', a['href']).url
                logger.debug("Baidu Found: %s" % url)
                yield url
        except:
            yield None

def _360so(search, page):
    for n in range(1, page + 1):
        base_url = 'https://www.so.com/s?q=' + str(quote(search)) + '&pn=' + str(n) + '&fr=so.com'
        try:
            r = mycurl('get', base_url)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('li.res-list > h3 > a'):
                url1 = mycurl('get', a['href'])
                url = re.findall("URL='(.*?)'", url1.text)[0] if re.findall("URL='(.*?)'", url1.text) else url1.url
                logger.debug("360so Found: %s" % url)
                yield url
        except:
            yield None

def _bing(search, page):
    for n in range(1, (page * 10) + 1, 10):
        base_url = 'http://cn.bing.com/search?q=' + str(quote(search)) + '&first=' + str(n)
        try:
            r = mycurl('get', base_url)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('li.b_algo > div.b_algoheader > a'):
                url = a['href']
                logger.debug("Bing Found: %s" % url)
                yield url
        except:
            yield None

def _google_api(search, page):
    '''
        https://console.developers.google.com
        https://developers.google.com/custom-search/v1/cse/list
        poc-t search_enging 011385053819762433240:ljmmw2mhhau
        https://cse.google.com.hk/cse?cx=011385053819762433240:ljmmw2mhhau&gws_rd=cr
    '''
    try:
        developer_key =  conf['config']['google_api']['developer_key']
        search_enging= conf['config']['google_api']['search_enging']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: google_api, please check the config in tentacle.conf."))
    anslist = []
    for p in range(0,page):
        base_url = 'https://www.googleapis.com/customsearch/v1?cx={0}&key={1}&num=10&start={2}&q={3}'.format(search_enging,developer_key,str(p * 10 +1),search)

        try:
            _proxies = None
            if conf['config']['proxy']['proxy'].lower() == 'true':
                try:
                    _proxies = {
                        'http': conf['config']['proxy']['http_proxy'],
                        'https': conf['config']['proxy']['https_proxy']
                    }
                except:
                    logger.error("Error http(s) proxy: %s or %s." % (conf['config']['proxy']['http_proxy'], conf['config']['proxy']['https_proxy']))
            res = mycurl('get',base_url, proxies=_proxies,timeout=10)
        except:
            res = None
        if res != None:
            if int(res.status_code) == 200:
                res_json = json.loads(res.text)
                try:
                    for item in res_json.get('items'):
                        anslist.append(item.get('link'))
                except:
                    break
            else:
                logger.error("Error google api access, and api rate limit 100/day, maybe you should pay money and enjoy service.")
                break
    return anslist


def _zoomeye_api(search, page, z_type):
    """
        app:"Drupal" country:"JP"
        curl -X POST https://api.zoomeye.org/user/login -d '
        {
        "username": "username@qq.com",
        "password": "password"
        }'
    """
    headers = {}
    url_login = 'https://api.zoomeye.org/user/login'
    try:
        data = {
            'username': conf['config']['zoomeye_api']['username'],
            'password': conf['config']['zoomeye_api']['password']
        }
        res = mycurl("post", url_login, json=data, headers=headers)
        if res == None :
            sys.exit(logger.error("Zoomeye api is not available."))
        headers["Authorization"] = "JWT " + json.loads(res.text)['access_token']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: zoomeye_api, please check the config in tentacle.conf."))
    except AttributeError as e :
        sys.exit(logger.error("Zoomeye api error: the response is none."))
    except Exception as e:
        sys.exit(logger.error("Zoomeye api error: %s" %type(e).__name__))
    if z_type.lower() == 'web':
        url_api = "https://api.zoomeye.org/web/search"
    elif z_type.lower() == 'host':
        url_api = "https://api.zoomeye.org/host/search"
    else:
        logger.error("Error zoomeye api with type {0}.".format(z_type))
        return None
    logger.sysinfo("Using zoomeye api with type {0}.".format(z_type))
    for n in range(1, page+1):
        logger.debug("Find zoomeye url of %d page..." % int(n))
        try:
            data = {'query': search, 'page': str(n)}
            res = mycurl("get", url_api, params=data, headers=headers)
            if int(res.status_code) == 422:
                sys.exit(logger.error("Error zoomeye api token."))
            if z_type.lower() == 'web':
                result = re.compile('"url": "(.*?)"').findall(res.text)
            elif z_type.lower() == 'host':
                result = [str(item['ip']) + ':' + str(item['portinfo']['port']) for item in json.loads(res.text)['matches']]
            logger.debug("Zoomeye Found: %s" % result)
            yield result
        except Exception:
            yield []

def _shodan_api(search, page):
    '''
        Please input your Shodan API Key (https://account.shodan.io/).
    '''
    try:
        token = conf['config']['shodan_api']['token']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: shodan_api, please check the config in tentacle.conf."))

    logger.sysinfo("Using shodan api...")
    anslist = []
    for p in range(1,page+1):
        logger.debug("Find shodan url of %d page..." % int(p))
        _proxies = None
        if conf['config']['proxy']['proxy'].lower() == 'true':
            try:
                _proxies = {
                    'http': conf['config']['proxy']['http_proxy'],
                    'https': conf['config']['proxy']['https_proxy']
                }
            except:
                logger.error("Error http(s) proxy: %s or %s." % (
                    conf['config']['proxy']['http_proxy'], conf['config']['proxy']['https_proxy']))
        try:
            api = shodan.Shodan(token, proxies=_proxies)
            result = api.search(query=search, page=p)
        except shodan.APIError as e:
            logger.error("Error shodan api access, maybe you should pay $49 and enjoy service.")
            return anslist

        total = result.get('total')
        if total == 0:
            logger.error("Found 0 target.")
            return anslist
        else :
            for match in result.get('matches'):
                target = match.get('ip_str') + ':' + str(match.get('port'))
                logger.debug("Shodan Found: %s" % target)
                anslist.append(target)

    return anslist

def _fofa_api(search, page, flag = True):
    '''
           https://fofa.so/api#auth
    '''
    url_login = 'https://fofa.so/api/v1/search/all'
    result = []
    try:
        email = conf['config']['fofa_api']['email']
        key = conf['config']['fofa_api']['token']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: zfofa_api, please check the config in tentacle.conf."))
    if flag:
        logger.sysinfo("Using fofa api...")
    search = str(base64encode(bytes(search, 'utf-8')),'utf-8')
    for p in range(1,page+1):
        logger.debug("Find fofa url of %d page..." % int(p))
        res = mycurl('post',url_login + '?email={0}&key={1}&page={2}&qbase64={3}'.format(email, key,p, search))
        if res !=None :
            if int(res.status_code) == 401:
                sys.exit(logger.error("Error fofa api access, maybe you should pay fofa coin and enjoy service."))
            else:
                res_json = json.loads( res.text)
                if res_json["error"] is None:
                    for item in res_json.get('results'):
                        logger.debug("Fofa Found: %s" % item[0])
                        result.append(item[0])
    return result

def _fofa_api_today_poc(page):
    target_list = []
    url = "https://fofa.so/about_client"
    res =  mycurl('get',url)
    if res != None:
        poc_soup = BeautifulSoup(res.content,'lxml')
        poc_result_name = poc_soup.select('body > div.fdo > div:nth-of-type(3) > div > div > ul > li:nth-of-type(1)')
        poc_result_raw = poc_soup.select('body > div.fdo > div:nth-of-type(3) > div > div > ul > li:nth-of-type(4) > a')
        for i in range(len(poc_result_name)):
            result_name = str(poc_result_name[i])[11:-5]
            result_raw = str(poc_result_raw[i])[str(poc_result_raw[i]).find(';">'):-4];result_raw = result_raw.replace(';">','')
            logger.sysinfo("Search fofa api %s: %s"%(result_name,result_raw))
            matchObj = re.search( r'[a-zA-Z0-9]+', result_name)
            if matchObj:
                server =  matchObj.group().lower()
                for z in _fofa_api(result_raw, page, False):
                    target_list.append((z, server))
            else:
                for z in _fofa_api(result_raw, page, False):
                    target_list.append(z, None)

    return target_list

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
    headers = {}
    url_api = "https://api.github.com/search/code?sort=updated&order=desc&per_page=%s&q=" %per_page_limit
    try:
        token = conf['config']['github_api']['token']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: github_api, please check the config in tentacle.conf."))
    headers["Authorization"] = "token " + token
    resp = mycurl('get',url_api + search, headers = headers, timeout=github_timeout)
    if resp!=None and resp.status_code == 200:
        logger.sysinfo("Using github api...")
        res_json = json.loads(resp.content)
        total = res_json["total_count"]
        logger.sysinfo("Found github url: %d"%int(total))
        page_num = (total // per_page_limit) + 1
        page_num = page_num if page < page_num else page
        git_urls = []
        for p in range(1,page_num + 1):
            # Search url
            _url_api = "https://api.github.com/search/code?sort=updated&order=desc&page=%d&per_page=%s&q=" % (p,per_page_limit)
            _resp = mycurl('get',_url_api + search, headers=headers, timeout=github_timeout)
            if _resp!=None and _resp.status_code == 200:
                logger.debug("Find github url of %d page..." % int(p))
                try:
                    _res_json = json.loads(_resp.content)
                    for i in range(len(_res_json['items'])):
                        git_urls.append(_res_json['items'][i]["html_url"])
                except:
                    pass
            elif _resp!=None and int(_resp.status_code) == 422:
                logger.error("Warning: github api access rate limit 20/minute, 5000/hour, 1000 search results.")
                logger.error("Error github api token. Wait for a minute.")

                # Access url and match, 既然限制了，那就干点其他事情。
                logger.sysinfo("So, this program will access target url and wait for rate limit. ")
                git_urls = list(set(git_urls))
                for url in git_urls:
                    try:
                        _resp = mycurl('get',url,timeout=github_timeout)
                    except:
                        _resp = None
                    if _resp and _resp.status_code == 200:

                        for i in InformationRegex:
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
                    elif _resp and _resp.status_code == 404:
                        pass
                    else :
                        logger.error(_resp.text)
                        logger.error(_resp.status_code)
                        time.sleep(60)
                git_urls = []
            elif _resp!=None and int(_resp.status_code) == 403:
                p = p - 1
                logger.error("Too many times for access. So we should wait for ten minute.")
                time.sleep(60*10)
            else:
                p = p - 1
                logger.error(_resp.text)
                logger.error(_resp.status_code)
                time.sleep(60)
    elif int(resp.status_code) == 422:
        sys.exit(logger.error("Error github api token."))
    return []

def _ceye_verify_api(filter, t = 'dns'):
    try:
        token = conf['config']['ceye_api']['token']
    except KeyError:
        logger.error("Load tentacle config error: ceye_api, please check the config in tentacle.conf.")
        return False
    filter = filter.replace('http://','')[0:20]
    url = "http://api.ceye.io/v1/records?token={token}&type={type}&filter={filter}".format(token = token,type = t,filter = filter)
    res =  mycurl('get',url)
    if res == None:
        logger.error("The ceye api is unavailable.!")
    elif res.status_code == 503:
        logger.error("The ceye api does not support such high frequency requests for the time being. Please reduce the thread to run again by --thread 5")
    elif filter in res.text:
        return True

    return False

def _ceye_dns_api(t = 'url'):
    '''

    :return:  identifier
    '''
    try:
        identifier = conf['config']['ceye_api']['identifier']
    except KeyError:
        logger.error("Load tentacle config error: ceye_api, please check the config in tentacle.conf.")
        return None
    target = random_string() + '.'+identifier
    if t == 'url':
        return "http://" + target
    else:
        return target