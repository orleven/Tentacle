#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import json
from lib.core.env import *
from lib.core.g import log
from lib.core.g import conf
from lib.util.aiohttputil import ClientSession
from lib.util.cipherutil import base64encode

async def get_fofa_api(search, page=40):
    """
    https://fofa.so/api#auth
    """
    url_login = 'https://fofa.info/api/v1/search/all'
    email = conf.fofa.email
    key = conf.fofa.token
    search = str(base64encode(search))
    async with ClientSession() as session:
        for p in range(1, page+1):
            log.debug("Find fofa url of %d page..." % int(p))
            async with session.get(url=url_login + '?email={0}&key={1}&page={2}&qbase64={3}'.format(email, key, p, search)) as res:
                if res:
                    if int(res.status) == 401:
                        log.error("Error fofa api access, maybe you should pay fofa coin and enjoy service.")
                    else:
                        text = await res.text()
                        if text:
                            res_json = json.loads(text)
                            if res_json.get('errmsg', None):
                                log.error(f"Error fofa api access, error {res_json.get('errmsg', None)}")
                            if len(res_json.get('results', [])) == 0:
                                break
                            for item in res_json.get('results', []):
                                log.debug("Fofa Found: %s" % item[0])
                                yield item[0]

