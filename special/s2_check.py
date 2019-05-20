#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re
import time

_ERROR_KEYS = ['Struts Problem Report','org.apache.struts2','struts.devMode','struts-tags',
              'There is no Action mapped for namespace']

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'struts scan'
        self.keyword = ['struts2', 'web']
        self.info = 'struts scan.'
        self.type = 'info'
        self.level = 'info'
        Script.__init__(self, target=target, server_type=self.server_type)


    def prove(self):
        self.get_url()
        # _status_flag = 5 # 暂定
        if self.base_url:
            test = self._gethtml(self.url)
            if test['code'] != 0:
                funlist = [self._checkDevMode,self._checkBySuffix,self._checActionsErrors,self._checkCheckBox,self._checkl18n]
                for fun in funlist:
                    flag = fun(self.base_url)
                    info = fun.__name__
                    if flag:
                        self.flag = 1
                        self.req.append({"flag": info})
                        self.res.append({"info": "struts_by" + info, "key": info})
                        break

    def _gethtml(self, url):
        try:
            u = self.curl('get', url)
            content = u.text
            return {"html": content, "code": u.status_code, "url": url}
        except Exception as e:
            # print(e)
            # _status_flag = _status_flag - 1
            return {"html": "", "code": 0, "url": url}
            # return _get_html_phantomJS(url)

    # check suffix :.do,.action
    def _checkBySuffix(self,url):

        info = self._gethtml(url)
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
    def _checkDevMode(self,url):
        target_url = url+"/struts/webconsole.html"
        info = self._gethtml(target_url)

        if info['code'] == 200 and "Welcome to the OGNL console" in info['html']:
            return True
        else:
            return False

    # check Error Messages.
    def _checActionsErrors(self,url):
        test_tmpurls = []
        test_tmpurls.append(url+"/?actionErrors=1111")
        test_tmpurls.append(url+"/tmp2017.action")
        test_tmpurls.append(url + "/tmp2017.do")
        test_tmpurls.append(url + "/system/index!testme.action")
        test_tmpurls.append(url + "/system/index!testme.do")

        for test_url in test_tmpurls:
            info = self._gethtml(test_url)
            for error_message in _ERROR_KEYS:
                if error_message in info['html'] and info['code'] == 500:
                    return True
        return False

    # check CheckboxInterceptor.
    def _checkCheckBox(self,url):
        for match in re.finditer(r"((\A|[?&])(?P<parameter>[^_]\w*)=)(?P<value>[^&#]+)", url):

            info = self._gethtml(url.replace(match.group('parameter'), "__checkbox_"+match.group('parameter')))
            check_key = 'name="{}"'.format(match.group('parameter'))
            check_value = 'value="false"'

            html = info['html']
            matchs_inputTags = re.findall(r"""<\s*input[^>]*>""", html,re.IGNORECASE)
            for input_tag in matchs_inputTags:
                if check_key in input_tag and check_value in input_tag:
                    return True

        return False



    def _checkl18n(self,target):
        info_orgi = self._gethtml(target)
        time.sleep(0.5)
        info_zhCN = self._gethtml(target+"?"+'request_locale=zh_CN')
        time.sleep(0.5)
        info_enUS = self._gethtml(target+"?"+ 'request_locale=en_US')
        time.sleep(0.5)

        if "request_locale=zh_CN" in info_orgi['html'] and "request_locale=en_US" in info_orgi['html']:
            return True

        if abs(len(info_zhCN['html']) - len(info_enUS['html'])) > 1024:
            return True

        return False


