#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import json
from lib.core.g import log
from lib.core.g import conf
from lib.util.aiohttputil import ClientSession

async def get_dnslog_recode(domain=None):
    """请求dnslog recode"""

    url = conf.dnslog.dnslog_api_url
    api_key = conf.dnslog.dnslog_api_key

    headers = {'API-Key': api_key, 'Content-Type': "application/json", }
    if domain is None:
        return False

    data = {"domain": domain, "ip": "", "per_page": 10000, "page": 1}
    dnslog_list = []

    msg = "response is null."
    try:
        async with ClientSession() as session:
            async with session.post(url, json=data, headers=headers, allow_redirects=False) as res:
                if res and res.status == 200:
                    content = await res.text()
                    if content:
                        dnslog_list = json.loads(content).get("data", {}).get("res", [])
                        return dnslog_list
                    else:
                        msg = "response is error."
    except Exception as e:
        msg = str(e)
        if "release" in msg:
            msg = 'timeout'
    log.error(f"Error api request, url: {url}, error: {msg}")
    return dnslog_list