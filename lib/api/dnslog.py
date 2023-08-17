#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven
import asyncio
import json
from lib.core.g import log
from lib.core.g import conf
from lib.util.aiohttputil import ClientSession
from lib.util.util import get_time
from lib.util.util import get_timestamp
from lib.util.util import random_lowercase_digits

async def dnslog_hander(driver=None):
    if conf.dnslog.dnslog_api_func == 'celestion':
        async for dnslog_recode in get_dnslog_recode_by_celestion():
            yield dnslog_recode
    if conf.dnslog.dnslog_api_func == 'ceye':
        async for dnslog_recode in get_dnslog_recode_by_ceye():
            yield dnslog_recode
    else:
        async for dnslog_recode in get_dnslog_recode_by_default(driver):
            yield dnslog_recode


async def get_dnslog_recode_by_ceye():
    """请求dnslog recode"""

    temp = random_lowercase_digits(5)
    conf.dnslog.dnslog_top_domain = f'{temp}.{conf.dnslog.dnslog_top_domain}'
    domain = conf.dnslog.dnslog_top_domain
    api_key = conf.dnslog.dnslog_api_key
    url = f"http://api.ceye.io/v1/records?token={api_key}&type=dns&filter={temp}"

    headers = {}

    dnslog_laster = get_time()
    while True:
        temp = get_time(get_timestamp() - conf.dnslog.dnslog_async_time)
        if temp > dnslog_laster:
            dnslog_laster = get_time()
            msg = "response is null."
            try:
                async with ClientSession() as session:
                    async with session.get(url, headers=headers, allow_redirects=False) as res:
                        if res:
                            if res.status == 200:
                                content = await res.text()
                                if content:
                                    dnslog_list = json.loads(content).get("data", [])
                                    for recode_domain in dnslog_list:
                                        yield recode_domain.get("name", None)
                                else:
                                    msg = "response is error."
                                    log.error(f"Error api request, url: {url}, error: {msg}")
                            else:
                                log.error("The ceye api does not support such high frequency requests for the time being.")
                        else:
                            log.error(f"Error api request, url: {url}, error: {msg}")
            except Exception as e:
                msg = str(e)
                if "release" in msg:
                    msg = 'timeout'
                log.error(f"Error api request, url: {url}, error: {msg}")
        await asyncio.sleep(0.1)



async def get_dnslog_recode_by_default(interactsh_client):

    custom_server = conf.dnslog.dnslog_api_url
    token = conf.dnslog.dnslog_api_key
    interactsh_client.config(custom_server, token)
    conf.dnslog.dnslog_top_domain = await interactsh_client.register()

    dnslog_laster = get_time()
    while True:
        temp = get_time(get_timestamp() - conf.dnslog.dnslog_async_time)
        if temp > dnslog_laster:
            dnslog_laster = get_time()
            recode_list = await interactsh_client.poll()
            for recode in recode_list:
                recode_domain = recode.get("full-id", None)
                if recode_domain:
                    recode_domain += '.' + interactsh_client.server
                    yield recode_domain
        await asyncio.sleep(0.1)

async def get_dnslog_recode_by_celestion():
    """请求dnslog recode"""

    url = conf.dnslog.dnslog_api_url
    api_key = conf.dnslog.dnslog_api_key
    conf.dnslog.dnslog_top_domain = f'{random_lowercase_digits(32)}.{conf.dnslog.dnslog_top_domain}'
    domain = conf.dnslog.dnslog_top_domain

    headers = {'API-Key': api_key, 'Content-Type': "application/json", }
    data = {"domain": domain, "ip": "", "per_page": 10000, "page": 1}

    dnslog_laster = get_time()
    while True:
        temp = get_time(get_timestamp() - conf.dnslog.dnslog_async_time)
        if temp > dnslog_laster:
            dnslog_laster = get_time()
            msg = "response is null."
            try:
                async with ClientSession() as session:
                    async with session.post(url, json=data, headers=headers, allow_redirects=False) as res:
                        if res and res.status == 200:
                            content = await res.text()
                            if content:
                                dnslog_list = json.loads(content).get("data", {}).get("res", [])
                                for recode_domain in dnslog_list:
                                    yield recode_domain.get("domain", None)
                            else:
                                msg = "response is error."
                                log.error(f"Error api request, url: {url}, error: {msg}")
                        else:
                            log.error(f"Error api request, url: {url}, error: {msg}")
            except Exception as e:
                msg = str(e)
                if "release" in msg:
                    msg = 'timeout'
                log.error(f"Error api request, url: {url}, error: {msg}")
        await asyncio.sleep(0.1)

# async def get_dnslog_recode(domain=None):
#     """请求dnslog recode"""
#
#     url = conf.dnslog.dnslog_api_url
#     api_key = conf.dnslog.dnslog_api_key
#
#     headers = {'API-Key': api_key, 'Content-Type': "application/json", }
#     if domain is None:
#         return False
#
#     data = {"domain": domain, "ip": "", "per_page": 10000, "page": 1}
#     dnslog_list = []
#     msg = "response is null."
#     try:
#         async with ClientSession() as session:
#             async with session.post(url, json=data, headers=headers, allow_redirects=False) as res:
#                 if res and res.status == 200:
#                     content = await res.text()
#                     if content:
#                         dnslog_list = json.loads(content).get("data", {}).get("res", [])
#                         return dnslog_list
#                     else:
#                         msg = "response is error."
#     except Exception as e:
#         msg = str(e)
#         if "release" in msg:
#             msg = 'timeout'
#     log.error(f"Error api request, url: {url}, error: {msg}")
#     return dnslog_list