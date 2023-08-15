#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import re
import json
from lib.core.g import log
from lib.core.g import conf
from lib.util.aiohttputil import ClientSession

async def get_zoomeye_api(search, page=40, z_type="host"):
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
            'username': conf.zoomeye.username,
            'password': conf.zoomeye.password,
        }
        async with ClientSession() as session:
            async with session.post(url=url_login, json=data, headers=headers) as res:
                if res:
                    text = await res.text()
                    headers["Authorization"] = "JWT " + json.loads(text)['access_token']
    except AttributeError as e :
        log.error("Zoomeye api error: the response is none.")
    except Exception as e:
        log.error("Zoomeye api error: %s" %type(e).__name__)
    if z_type.lower() == 'web':
        url_api = "https://api.zoomeye.org/web/search"
    elif z_type.lower() == 'host':
        url_api = "https://api.zoomeye.org/host/search"
    else:
        url_api = None
        log.error("Error zoomeye api with type {0}.".format(z_type))
        yield None
    log.info("Using zoomeye api with type {0}.".format(z_type))
    async with ClientSession() as session:
        for n in range(1, page+1):
            log.debug("Find zoomeye url of %d page..." % int(n))
            try:
                data = {'query': search, 'page': str(n)}
                async with session.get(url=url_api, params=data, headers=headers) as res:
                    if res:
                        text = await res.text()
                        if int(res.status) == 422:
                            log.error("Error zoomeye api token.")
                        if z_type.lower() == 'web':
                            result = re.compile('"url": "(.*?)"').findall(text)
                        elif z_type.lower() == 'host':
                            result = [str(item['ip']) + ':' + str(item['portinfo']['port']) for item in json.loads(text)['matches']]
                        log.debug("Zoomeye Found: %s" % result)
                        if isinstance(result, list):
                            for temp in result:
                                yield temp
                        else:
                            yield result
            except Exception:
                yield []

