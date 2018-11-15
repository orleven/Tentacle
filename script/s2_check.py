#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

_ERROR_KEYS = ['Struts Problem Report','org.apache.struts2','struts.devMode','struts-tags',
              'There is no Action mapped for namespace']

def get_script_info(data=None):
    script_info = {
        "name": "struts scan",
        "info": "This is a test.",
        "level": "low",
        "type": "info",
        "author": "orleven",
        "url": "",
        "keyword": "tag:iis",
        "source": 1
    }
    return script_info

def prove(data):
    '''
    data = {
        "target_host":"",
        "target_port":"",
        "proxy":"",
        "dic_one":"",
        "dic_two":"",
        "cookie":"",
        "url":"",
        "flag":"",
        "data":"",
        "":"",

    }

    '''


    headers = {}
    headers[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    headers['Accept-Language'] = 'en-us;q=0.5,en;q=0.3'
    status, data, base_url = _url_deal(headers, data)
    headers['Referer'] = base_url
    if status:
        funlist = [_checkDevMode,_checkBySuffix,_checActionsErrors,_checkCheckBox,_checkl18n]
        for fun in funlist:
            flag = fun(base_url,headers)
            info = fun.__name__
            if flag:
                data['flag'] = True
                data['data'].append({"flag": info})
                data['res'].append({"info": "struts_by"+info, "key": info})
                break
    return data


# check suffix :.do,.action
def _checkBySuffix(url,headers):
    import re
    info = _gethtml(url, headers)
    if info['code'] == 404:
        return False
    html = info['html']

    matchs_action = re.findall(r"""(['"]{1})(/?((?:(?!\1|\n|http(s)?://).)+)\.action)(\?(?:(?!\1).)*)?\1""", html,
                        re.IGNORECASE)

    matchs_do = re.findall(r"""(['"]{1})(/?((?:(?!\1|\n|http(s)?://).)+)\.do)(\?(?:(?!\1).)*)?\1""", html,
                        re.IGNORECASE)

    if len(matchs_do)+len(matchs_action)> 0 and (".action" in str(matchs_action) or ".do" in str(matchs_do)):
        return True
    else:
        return False


# check devMode page
def _checkDevMode(url,headers):
    target_url = url+"/struts/webconsole.html"
    info = _gethtml(target_url,headers)

    if info['code'] == 200 and "Welcome to the OGNL console" in info['html']:
        return True
    else:
        return False

# check Error Messages.
def _checActionsErrors(url,headers):
    test_tmpurls = []

    test_tmpurls.append(url+"/?actionErrors=1111")
    test_tmpurls.append(url+"/tmp2017.action")
    test_tmpurls.append(url + "/tmp2017.do")
    test_tmpurls.append(url + "/system/index!testme.action")
    test_tmpurls.append(url + "/system/index!testme.do")

    for test_url in test_tmpurls:
        info = _gethtml(test_url,headers)
        for error_message in _ERROR_KEYS:
            if error_message in info['html'] and info['code'] == 500:
                print ("[+] found error_message:",error_message)
                return True
    return False

# check CheckboxInterceptor.
def _checkCheckBox(url,headers):
    import re


    for match in re.finditer(r"((\A|[?&])(?P<parameter>[^_]\w*)=)(?P<value>[^&#]+)", url):

        info = _gethtml(url.replace(match.group('parameter'), "__checkbox_"+match.group('parameter')),headers)
        check_key = 'name="{}"'.format(match.group('parameter'))
        check_value = 'value="false"'

        html = info['html']
        matchs_inputTags = re.findall(r"""<\s*input[^>]*>""", html,re.IGNORECASE)
        for input_tag in matchs_inputTags:
            if check_key in input_tag and check_value in input_tag:
                return True

    return False



def _checkl18n(target,headers):
    import time
    info_orgi = _gethtml(target,headers)
    time.sleep(0.5)
    info_zhCN = _gethtml(target+"?"+'request_locale=zh_CN',headers)
    time.sleep(0.5)
    info_enUS = _gethtml(target+"?"+ 'request_locale=en_US',headers)
    time.sleep(0.5)

    if "request_locale=zh_CN" in info_orgi['html'] and "request_locale=en_US" in info_orgi['html']:
        return True

    if abs(len(info_zhCN['html']) - len(info_enUS['html'])) > 1024:
        return True

    return False

def _gethtml(url,headers):
    import requests
    try:
        u = requests.get(url, timeout=3, headers=headers, allow_redirects=True)
        content = u.text
        return {"html":content,"code":u.status_code,"url":url}

    except Exception as e:
        # print(e)
        return {"html":"", "code":500, "url":url}
        # return _get_html_phantomJS(url)

# 使用PhantomJS获取网页源码
def _get_html_phantomJS(url):
    import time
    try:
        from selenium import webdriver
        dr = webdriver.PhantomJS()
        dr.get(url)
        time.sleep(2)
        return {"html": dr.page_source, "code": 200, "url": url}

    except Exception as e:
        # http://phantomjs.org/
        print (e)
        return {"html":"", "code":500, "url":url}

def _url_deal(headers,data):
    import urllib.parse
    if 'url' in data.keys() and data['url'] != None:
        protocol, s1 = urllib.parse.splittype(data['url'])
        host, s2 = urllib.parse.splithost(s1)
        host, port = urllib.parse.splitport(host)
        port = port if port != None else 443 if protocol == 'https' else 80
        base_url = protocol + "://" + host + ":" + str(port)+'/'
        return _curl_status(data,base_url,headers),data,base_url
    else:
        if data['target_port'] == 0:
            target = data['target_host']
        else:
            target = data['target_host'] + ":" + str(data['target_port'])
        for pro in ['http://', "https://"]:
            if _curl_status(data, pro + target, headers):
                data['url'] = base_url = pro + target+'/'
                return True, data, base_url
    return False,data,"None"


def _curl_status(data, url, headers):
    import requests
    requests.packages.urllib3.disable_warnings()
    try:
        requests.get(url, headers=headers, verify=False, timeout=5)
        return True
    except:
        return False