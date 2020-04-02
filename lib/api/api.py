#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re
import json
import sys
from bs4 import BeautifulSoup
from urllib.parse import quote
from lib.utils.cipher import base64encode
from lib.utils.connect import ClientSession
from lib.core.data import logger
from lib.core.data import conf
from lib.core.enums import API_TYPE
from lib.core.common import random_string

async def search_api(search,type, page = 40):
    target_list = []
    try:
        if type == API_TYPE.ZOOMEYE:
            for type in ['host','web']:
                async for z in _zoomeye_api(search, page, type):
                    for url in z:
                        target_list.append(url)

        elif type == API_TYPE.SHODAN:
            async for z in _shodan_api(search, page):
                target_list.append(z)

        elif type == API_TYPE.FOFA:
            async for z in _fofa_api(search, page):
                target_list.append(z)

        # elif type == API_TYPE.FOFA_TODAY_POC:
        #     async for z in _fofa_api_today_poc(page):
        #         target_list.append(z)

        elif type == API_TYPE.GOOGLE:
            async for z in _google_api(search, page):
                target_list.append(z)

        elif type == API_TYPE.OTHER_SEARCH_ENGINE:
            async for url in _baidu(search, page):
                target_list.append(url)

            async for url in _360so(search, page):
                target_list.append(url)

            async for url in _bing(search, page):
                target_list.append(url)

    except KeyboardInterrupt:
        sys.exit(logger.error("Exit by user."))

    if isinstance(target_list,tuple):
        return target_list
    return list(set(target_list))

async def _baidu(search, page):
    async with ClientSession() as session:
        for n in range(0, page * 10, 10):
            base_url = 'https://www.baidu.com/s?wd=' + str(quote(search)) + '&oq=' + str(
                quote(search)) + '&ie=utf-8' + '&pn=' + str(n)
            async with session.get(url=base_url) as response:
                if response:
                    res = await response.text()
                    soup = BeautifulSoup(res, "html.parser")
                    for a in soup.select('div.c-container > h3 > a'):
                        async with session.get(url=a['href']) as response:
                            if response:
                                url = str(response.url)
                                logger.debug("Baidu Found: %s" % url)
                                yield url

async def _360so(search, page):
    async with ClientSession() as session:
        for n in range(1, page + 1):
            base_url = 'https://www.so.com/s?q=' + str(quote(search)) + '&pn=' + str(n) + '&fr=so.com'
            async with session.get(url=base_url) as response:
                if response:
                    res = await response.text()
                    soup = BeautifulSoup(res, "html.parser")
                    for a in soup.select('li.res-list > h3 > a'):
                        async with session.get(url=a['href']) as response:
                            if response:
                                res = await response.text()
                                url = re.findall("URL='(.*?)'", res)[0] if re.findall("URL='(.*?)'", res) else str(response.url)
                                logger.debug("360so Found: %s" % url)
                                yield url

async def _bing(search, page):
    async with ClientSession() as session:
        for n in range(1, (page * 10) + 1, 10):
            base_url = 'http://cn.bing.com/search?q=' + str(quote(search)) + '&first=' + str(n)
            async with session.get(url=base_url) as response:
                if response:
                    res = await response.text()
                    soup = BeautifulSoup(res, "html.parser")
                    for a in soup.select('li.b_algo > div.b_algoheader > a'):
                        url = a['href']
                        logger.debug("Bing Found: %s" % url)
                        yield url


async def _google_api(search, page):
    '''
        https://console.developers.google.com
        https://developers.google.com/custom-search/v1/cse/list
        poc-t search_enging 011385053819762433240:ljmmw2mhhau
        https://cse.google.com.hk/cse?cx=011385053819762433240:ljmmw2mhhau&gws_rd=cr
    '''
    try:
        developer_key =  conf['google_api']['developer_key']
        search_enging= conf['google_api']['search_enging']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: google_api, please check the config in tentacle.conf."))
    async with ClientSession() as session:
        for p in range(0,page):
            base_url = 'https://www.googleapis.com/customsearch/v1?cx={0}&key={1}&num=10&start={2}&q={3}'.format(search_enging,developer_key,str(p * 10 +1),search)
            async with session.get(url=base_url) as response:
                if response:
                    res = await response.text()
                    if int(response.status) == 200:
                        res_json = json.loads(res)
                        try:
                            for item in res_json.get('items'):
                                yield item.get('link')
                        except:
                            break
                    else:
                        logger.error("Error google api access, and api rate limit 100/day, maybe you should pay money and enjoy service.")
                        break


async def _zoomeye_api(search, page, z_type):
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
            'username': conf['zoomeye_api']['username'],
            'password': conf['zoomeye_api']['password']
        }
        async with ClientSession() as session:
            async with session.post(url=url_login, json=data, headers=headers) as response:
                if response:
                    res = await response.text()
                    headers["Authorization"] = "JWT " + json.loads(res)['access_token']
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
        url_api = None
        logger.error("Error zoomeye api with type {0}.".format(z_type))
        yield None
    logger.sysinfo("Using zoomeye api with type {0}.".format(z_type))
    async with ClientSession() as session:
        for n in range(1, page+1):
            logger.debug("Find zoomeye url of %d page..." % int(n))
            try:
                data = {'query': search, 'page': str(n)}
                async with session.get(url=url_api, params=data, headers=headers) as response:
                    if response:
                        res = await response.text()
                        if int(response.status) == 422:
                            sys.exit(logger.error("Error zoomeye api token."))
                        if z_type.lower() == 'web':
                            result = re.compile('"url": "(.*?)"').findall(res)
                        elif z_type.lower() == 'host':
                            result = [str(item['ip']) + ':' + str(item['portinfo']['port']) for item in json.loads(res)['matches']]
                        logger.debug("Zoomeye Found: %s" % result)
                        yield result
            except Exception:
                yield []

async def _shodan_api(search, page):
    '''
        Please input your Shodan API Key (https://account.shodan.io/).
    '''
    try:
        token = conf['shodan_api']['token']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: shodan_api, please check the config in tentacle.conf."))

    logger.sysinfo("Using shodan api...")
    url_api = 'https://api.shodan.io/shodan/host/search'
    async with ClientSession() as session:
        for n in range(1, page + 1):
            logger.debug("Find shodan url of %d page..." % int(n))
            data = {'query': search, 'page': str(n), 'key': token, 'minify': 1}
            async with session.get(url=url_api, params=data, timeout=None) as response:
                if response and response.status == 200:

                    result = b''
                    while True:
                        try:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            result += chunk
                        except:
                            break

                    try:
                        text = json.loads(result.decode())
                    except:
                        pass
                    else:
                        total = text.get('total')
                        if total == 0:
                            logger.error("Found 0 target.")
                        else:
                            for match in text.get('matches'):
                                target = match.get('ip_str') + ':' + str(match.get('port'))
                                logger.debug("Shodan Found: %s" % target)
                                yield target
                else:
                    sys.exit(logger.error("Error fofa api access."))

async def _fofa_api(search, page, flag = True):
    '''
           https://fofa.so/api#auth
    '''
    url_login = 'https://fofa.so/api/v1/search/all'
    try:
        email = conf['fofa_api']['email']
        key = conf['fofa_api']['token']
    except KeyError:
        sys.exit(logger.error("Load tentacle config error: zfofa_api, please check the config in tentacle.conf."))
    if flag:
        logger.sysinfo("Using fofa api...")

    search = str(base64encode(search))

    async with ClientSession() as session:
        for p in range(1,page+1):
            logger.debug("Find fofa url of %d page..." % int(p))
            async with session.post(url=url_login + '?email={0}&key={1}&page={2}&qbase64={3}'.format(email, key,p, search)) as response:
                if response !=None:
                    if int(response.status) == 401:
                        sys.exit(logger.error("Error fofa api access, maybe you should pay fofa coin and enjoy service."))
                    else:
                        res = await response.text()
                        if res !=None:
                            res_json = json.loads(res)
                            if res_json["error"] is None:
                                if len(res_json.get('results')) == 0:
                                    break
                                for item in res_json.get('results'):
                                    logger.debug("Fofa Found: %s" % item[0])
                                    yield item[0]

# async def _fofa_api_today_poc(page):
#     url = "https://fofa.so/about_client"
#     async with ClientSession() as session:
#         async with session.post(url=url) as response:
#             if response:
#                 res = await response.text()
#                 poc_soup = BeautifulSoup(res,'lxml')
#                 poc_result_name = poc_soup.select('body > div.fdo > div:nth-of-type(3) > div > div > ul > li:nth-of-type(1)')
#                 poc_result_raw = poc_soup.select('body > div.fdo > div:nth-of-type(3) > div > div > ul > li:nth-of-type(4) > a')
#                 for i in range(len(poc_result_name)):
#                     result_name = str(poc_result_name[i])[11:-5]
#                     result_raw = str(poc_result_raw[i])[str(poc_result_raw[i]).find(';">'):-4];result_raw = result_raw.replace(';">','')
#                     logger.sysinfo("Search fofa api %s: %s"%(result_name,result_raw))
#                     matchObj = re.search( r'[a-zA-Z0-9]+', result_name)
#                     if matchObj:
#                         server =  matchObj.group().lower()
#                         async for z in _fofa_api(result_raw, page, False):
#                             yield (z, server)
#                             # target_list.append((z, server))
#                     else:
#                         async for z in _fofa_api(result_raw, page, False):
#                             yield (z, None)


async def _ceye_verify_api(filter, t = 'dns'):
    try:
        token = conf['ceye_api']['token']
    except KeyError:
        logger.error("Load tentacle config error: ceye_api, please check the config in tentacle.conf.")
        return False
    if t != 'dns':
        t = 'http'
    filter = filter.replace('http://','')[0:20]
    url = "http://api.ceye.io/v1/records?token={token}&type={type}&filter={filter}".format(token = token,type = t,filter = filter)
    async with ClientSession() as session:
        async with session.get(url=url) as response:
            if response!=None:
                res = await response.text()
                if response == None:
                    logger.error("The ceye api is unavailable.!")
                elif response.status == 503:
                    logger.error("The ceye api does not support such high frequency requests for the time being. Please reduce the thread to run again by --thread 5")
                elif filter in res:
                    return True
    return False

def _ceye_dns_api(k='test', t = 'url'):
    '''

    :return:  identifier
    '''
    try:
        identifier = conf['ceye_api']['identifier']
    except KeyError:
        logger.error("Load tentacle config error: ceye_api, please check the config in tentacle.conf.")
        return None
    target = random_string() + '.' + k + '.'  +identifier
    if t == 'url' or t =='http':
        return "http://" + target
    else:
        return target