#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from requests.adapters import HTTPAdapter
import random
import requests
from requests import request
from lib.core.data import conf
from lib.core.data import logger
from lib.core.settings import USER_AGENTS
from lib.core.common import random_IP
from lib.core.common import get_safe_ex_string
from requests.exceptions import ConnectionError
from requests.exceptions import TooManyRedirects
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ReadTimeout
requests.packages.urllib3.disable_warnings()


def geturl(host, port, **kwargs):
    for pro in ['http://', "https://"]:
        _port = port if port != None and port != 0 else 443 if pro == 'https' else 80
        _pro = 'https://' if port == 443 else pro
        url = _pro + host + ":" + str(_port) + '/'
        res = curl('head', url, **kwargs)
        if res != None:
            if res.status_code == 400 and 'The plain HTTP request was sent to HTTPS port' in res.text:
                continue
            return url
    return None

def curl(method,url, **kwargs):
    headers = kwargs.get('headers')
    if headers == None:
        headers = {}
    headers['Accept-Charset'] = 'GB2312,utf-8;q=0.7,*;q=0.7'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
    headers['Referer'] = url
    if 'User-Agent' not in headers.keys():
        headers["User-Agent"] = random.choice(USER_AGENTS)
    # if 'X-Forwarded-For' not in headers.keys():
    #     headers['X-Forwarded-For'] = random_IP()
    kwargs.setdefault('headers',headers)
    if 'timeout' not in headers.keys():
        kwargs.setdefault('timeout',  int(conf['config']['basic']['timeout']))
    kwargs.setdefault('verify', False)
    max_retries = int(conf['config']['basic']['max_retries'])
    # if conf['config']['proxy']['proxy'].lower() == 'true':
    #     try:
    #         _proxies = {
    #             'http': conf['config']['proxy']['http_proxy'],
    #             'https': conf['config']['proxy']['https_proxy']
    #         }
    #         kwargs.setdefault('proxies', _proxies)
    #     except:
    #         logger.error("Error http(s) proxy: %s or %s." % (conf['config']['proxy']['http_proxy'],conf['config']['proxy']['https_proxy']))
    try:
        with requests.sessions.Session() as session:
            session.mount('http://', HTTPAdapter(max_retries=max_retries))
            session.mount('https://', HTTPAdapter(max_retries=max_retries))
            return session.request(method=method, url=url, **kwargs)
    except TooManyRedirects as e:
        kwargs.setdefault('allow_redirects', False)
        try:
            return request(method, url, **kwargs)
        except ChunkedEncodingError as e:
            return None
    except (ConnectionError,TimeoutError,ReadTimeout,ChunkedEncodingError)as e :
        pass
    except Exception as e:
        logger.error("Curl error: %s for %s" % (get_safe_ex_string(e),url))
    return None