#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re
import json
import sys
import shodan
from bs4 import BeautifulSoup
from urllib.parse import quote
from lib.utils.cipher import base64encode
from lib.utils.curl import curl
from lib.core.data import logger
from lib.core.data import conf
from lib.core.common import random_string

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

        elif 'target_google' in conf.keys():
            for z in _google_api(search, page):
                target_list.append(z)

    except KeyboardInterrupt:
        sys.exit(logger.error("Exit by user."))

    if isinstance(target_list,tuple):
        return target_list
    return list(set(target_list))

def search_engine(search,page = 10):
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
            r = curl('get',base_url)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('div.c-container > h3 > a'):
                url = curl('get', a['href']).url
                logger.debug("Baidu Found: %s" % url)
                yield url
        except:
            yield None

def _360so(search, page):
    for n in range(1, page + 1):
        base_url = 'https://www.so.com/s?q=' + str(quote(search)) + '&pn=' + str(n) + '&fr=so.com'
        try:
            r = curl('get', base_url)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('li.res-list > h3 > a'):
                url1 = curl('get', a['href'])
                url = re.findall("URL='(.*?)'", url1.text)[0] if re.findall("URL='(.*?)'", url1.text) else url1.url
                logger.debug("360so Found: %s" % url)
                yield url
        except:
            yield None

def _bing(search, page):
    for n in range(1, (page * 10) + 1, 10):
        base_url = 'http://cn.bing.com/search?q=' + str(quote(search)) + '&first=' + str(n)
        try:
            r = curl('get', base_url)
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
            # _proxies = None
            # if conf['config']['proxy']['proxy'].lower() == 'true':
            #     try:
            #         _proxies = {
            #             'http': conf['config']['proxy']['http_proxy'],
            #             'https': conf['config']['proxy']['https_proxy']
            #         }
            #     except:
            #         logger.error("Error http(s) proxy: %s or %s." % (conf['config']['proxy']['http_proxy'], conf['config']['proxy']['https_proxy']))
            # res = curl('get',base_url, proxies=_proxies,timeout=5)
            res = curl('get', base_url, timeout=5)
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
        res = curl("post", url_login, json=data, headers=headers)
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
            res = curl("get", url_api, params=data, headers=headers)
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
        res = curl('post',url_login + '?email={0}&key={1}&page={2}&qbase64={3}'.format(email, key,p, search))
        if res !=None :
            if int(res.status_code) == 401:
                sys.exit(logger.error("Error fofa api access, maybe you should pay fofa coin and enjoy service."))
            else:
                res_json = json.loads( res.text)
                if res_json["error"] is None:
                    if len(res_json.get('results')) ==0:
                        break
                    for item in res_json.get('results'):
                        logger.debug("Fofa Found: %s" % item[0])
                        result.append(item[0])
    return result

def _fofa_api_today_poc(page):
    target_list = []
    url = "https://fofa.so/about_client"
    res =  curl('get',url)
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
                    target_list.append((z, None))

    return target_list

def _ceye_verify_api(filter, t = 'dns'):
    try:
        token = conf['config']['ceye_api']['token']
    except KeyError:
        logger.error("Load tentacle config error: ceye_api, please check the config in tentacle.conf.")
        return False
    filter = filter.replace('http://','')[0:20]
    url = "http://api.ceye.io/v1/records?token={token}&type={type}&filter={filter}".format(token = token,type = t,filter = filter)
    res = curl('get',url)
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