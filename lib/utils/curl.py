#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'


import urllib3
import backoff
import random
import requests
from requests import request
from lib.core.data import conf
from lib.core.data import logger
from lib.core.common import random_IP
from lib.core.common import get_safe_ex_string
from requests.exceptions import ConnectionError
from requests.exceptions import TooManyRedirects
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ReadTimeout
from urllib3.connection import ConnectTimeoutError
from urllib3 import HTTPConnectionPool
requests.packages.urllib3.disable_warnings()

def mycurl(method,url, params = None, **kwargs):
    try:
        return _mycurl(method, url, params=params, **kwargs)
    except (ConnectionError,TimeoutError,ReadTimeout)as e :
        pass
    except Exception as e:
        logger.error("Curl error: %s for %s" % (e,url))
    return None

@backoff.on_exception(backoff.expo, (ConnectionError,TimeoutError,ReadTimeout), max_tries=3, max_time=30)
def _mycurl(method,url, params = None, **kwargs):
    headers = kwargs.get('headers')
    if headers == None:
        headers = {}
    headers['Accept-Charset'] = 'GB2312,utf-8;q=0.7,*;q=0.7'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
    headers['Referer'] = url
    if 'User-Agent' not in headers.keys():
        headers["User-Agent"] = random.choice(conf['config']['basic']['user_agent'])
    # if 'X-Forwarded-For' not in headers.keys():
    #     headers['X-Forwarded-For'] = random_IP()
    kwargs.setdefault('headers',headers)
    if 'timeout' not in headers.keys():
        kwargs.setdefault('timeout',  int(conf['config']['basic']['timeout']))
    kwargs.setdefault('verify', False)
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
        return request(method, url, params=params, **kwargs)
    except ChunkedEncodingError as e:
        return None
    except TooManyRedirects as e:
        kwargs.setdefault('allow_redirects', False)
        try:
            return request(method, url, params=params, **kwargs)
        except ChunkedEncodingError as e:
            return None
