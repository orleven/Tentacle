#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import json
from lib.core.g import log
from lib.core.g import conf
from lib.util.aiohttputil import ClientSession

async def get_google_api(search, page=40):
    """
        https://console.developers.google.com
        https://developers.google.com/custom-search/v1/cse/list
        poc-t search_enging 011385053819762433240:ljmmw2mhhau
        https://cse.google.com.hk/cse?cx=011385053819762433240:ljmmw2mhhau&gws_rd=cr
    """

    developer_key = conf.google.developer_key
    search_enging = conf.google.search_enging
    async with ClientSession() as session:
        for p in range(0, page):
            base_url = 'https://www.googleapis.com/customsearch/v1?cx={0}&key={1}&num=10&start={2}&q={3}'.format(search_enging,developer_key,str(p * 10 +1),search)
            async with session.get(url=base_url) as res:
                if res and res.status == 200:
                    res = await res.text()
                    res_json = json.loads(res)
                    try:
                        for item in res_json.get('items'):
                            yield item.get('link')
                    except:
                        break
                else:
                    log.error("Error google api access, and api rate limit 100/day, maybe you should pay money and enjoy service.")
                    break
