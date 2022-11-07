#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import re
from bs4 import BeautifulSoup
from lib.core.g import log
from urllib.parse import quote
from lib.util.aiohttputil import ClientSession

async def get_search_engine_api(search, page=40):
    # async for url in baidu(search, page):
    #     yield url

    async for url in so360(search, page):
        yield url

    async for url in bing(search, page):
        yield url

async def baidu(search, page):
    """
    baidu有防爬机制
    :param search:
    :param page:
    :return:
    """
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
                                log.debug("Baidu Found: %s" % url)
                                yield url

async def so360(search, page):
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
                                log.debug("360so Found: %s" % url)
                                yield url

async def bing(search, page):
    async with ClientSession() as session:
        for n in range(1, (page * 10) + 1, 10):
            base_url = 'http://cn.bing.com/search?q=' + str(quote(search)) + '&first=' + str(n)
            async with session.get(url=base_url) as response:
                if response:
                    res = await response.text()
                    soup = BeautifulSoup(res, "html.parser")
                    for a in soup.select('li.b_algo > div.b_title > a'):
                        url = a['href']
                        log.debug("Bing Found: %s" % url)
                        yield url
