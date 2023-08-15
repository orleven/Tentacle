#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import json
from lib.core.g import log
from lib.core.g import conf
from lib.util.aiohttputil import ClientSession

async def get_shodan_api(search, page=40):
    """
    Please input your Shodan API Key (https://account.shodan.io/).
    """
    token = conf.shodan.token
    log.debug("Using shodan api...")
    headers = {"User-Agent": "curl/7.77.0", "API-Key": "api"}
    url_api = 'https://api.shodan.io/shodan/host/search'
    async with ClientSession() as session:
        for n in range(1, page + 1):
            log.debug("Find shodan url of %d page..." % int(n))
            data = {'query': search, 'page': str(n), 'key': token, 'minify': 1}
            async with session.get(url=url_api, params=data, timeout=None, headers=headers) as res:
                if res and res.status == 200:
                    result = b''
                    while True:
                        try:
                            chunk = await res.content.read(1024)
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
                            log.error("Found 0 target.")
                        else:
                            for match in text.get('matches'):
                                target = match.get('ip_str') + ':' + str(match.get('port'))
                                log.debug("Shodan Found: %s" % target)
                                yield target
                else:
                    log.error("Error shodan api access.")
