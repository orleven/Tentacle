#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re
import time

_ERROR_KEYS = ['Struts Problem Report','org.apache.struts2','struts.devMode','struts-tags',
              'There is no Action mapped for namespace']


def info(data=None):
    info = {
        "name": "struts scan",
        "info": "This is a test.",
        "level": "low",
        "type": "info",
    }
    return info

def prove(data):
    data = init(data, 'web')
    # _status_flag = 5 # 暂定
    if data['base_url'] :
        test = _gethtml(data['url'])
        if test['code'] != 0:
            funlist = [_checkDevMode,_checkBySuffix,_checActionsErrors,_checkCheckBox,_checkl18n]
            for fun in funlist:
                flag = fun(data['base_url'])
                info = fun.__name__
                if flag:
                    data['flag'] = 1
                    data['data'].append({"flag": info})
                    data['res'].append({"info": "struts_by" + info, "key": info})
                    break
    return data



# check suffix :.do,.action
def _checkBySuffix(url):

    info = _gethtml(url)
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
def _checkDevMode(url):
    target_url = url+"/struts/webconsole.html"
    info = _gethtml(target_url)

    if info['code'] == 200 and "Welcome to the OGNL console" in info['html']:
        return True
    else:
        return False

# check Error Messages.
def _checActionsErrors(url):
    test_tmpurls = []
    test_tmpurls.append(url+"/?actionErrors=1111")
    test_tmpurls.append(url+"/tmp2017.action")
    test_tmpurls.append(url + "/tmp2017.do")
    test_tmpurls.append(url + "/system/index!testme.action")
    test_tmpurls.append(url + "/system/index!testme.do")

    for test_url in test_tmpurls:
        info = _gethtml(test_url)
        for error_message in _ERROR_KEYS:
            if error_message in info['html'] and info['code'] == 500:
                return True
    return False

# check CheckboxInterceptor.
def _checkCheckBox(url):
    for match in re.finditer(r"((\A|[?&])(?P<parameter>[^_]\w*)=)(?P<value>[^&#]+)", url):

        info = _gethtml(url.replace(match.group('parameter'), "__checkbox_"+match.group('parameter')))
        check_key = 'name="{}"'.format(match.group('parameter'))
        check_value = 'value="false"'

        html = info['html']
        matchs_inputTags = re.findall(r"""<\s*input[^>]*>""", html,re.IGNORECASE)
        for input_tag in matchs_inputTags:
            if check_key in input_tag and check_value in input_tag:
                return True

    return False



def _checkl18n(target):
    info_orgi = _gethtml(target)
    time.sleep(0.5)
    info_zhCN = _gethtml(target+"?"+'request_locale=zh_CN')
    time.sleep(0.5)
    info_enUS = _gethtml(target+"?"+ 'request_locale=en_US')
    time.sleep(0.5)

    if "request_locale=zh_CN" in info_orgi['html'] and "request_locale=en_US" in info_orgi['html']:
        return True

    if abs(len(info_zhCN['html']) - len(info_enUS['html'])) > 1024:
        return True

    return False

def _gethtml(url):
    try:
        u = curl('get',url)
        content = u.text
        return {"html":content,"code":u.status_code,"url":url}
    except Exception as e:
        # print(e)
        # _status_flag = _status_flag - 1
        return {"html":"", "code":0, "url": url}
        # return _get_html_phantomJS(url)


if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))