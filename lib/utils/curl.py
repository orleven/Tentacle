#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import backoff
import random
import requests
from requests import request
from lib.core.data import conf
from lib.core.data import logger
from lib.core.common import random_IP
from requests.exceptions import ConnectionError
from requests.exceptions import TooManyRedirects
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ReadTimeout
requests.packages.urllib3.disable_warnings()

@backoff.on_exception(backoff.expo, TimeoutError, max_tries=3)
def mycurl(method,url, params = None, **kwargs):
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
    kwargs.setdefault('timeout',  int(conf['config']['basic']['timeout']))
    kwargs.setdefault('verify', False)

    if conf['config']['proxy']['proxy'].lower() == 'true':
        try:
            _proxies = {
                'http': conf['config']['proxy']['http_proxy'],
                'https': conf['config']['proxy']['https_proxy']
            }
            kwargs.setdefault('proxies', _proxies)
        except:
            logger.error("Error http(s) proxy: %s or %s." % (conf['config']['proxy']['http_proxy'],conf['config']['proxy']['https_proxy']))
    try:
        return request(method, url, params=params, **kwargs)
    except ConnectionError as e:
        return None
    except ReadTimeout as e:
        return None
    except ChunkedEncodingError as e:
        return None
    except TooManyRedirects as e:
        kwargs.setdefault('allow_redirects', False)
        try:
            return request('get', url, params=params, **kwargs)
        except:
            return None
    except Exception as e:
        logger.error("Curl error: %s" % url)
        return None


