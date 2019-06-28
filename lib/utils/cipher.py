#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import string
import hashlib
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Util import number
from Crypto.PublicKey import RSA
from lib.utils.output import single_time_warn_message

try:
    import cPickle as pickle
except:
    import pickle
finally:
    import pickle as picklePy

def md5(message):
    obj = hashlib.md5()
    obj.update(message.encode(encoding='utf-8'))
    return obj.hexdigest()

def base64decode(value,table=None):
    b64_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    if table:
        return b64decode(str.translate(value,str.maketrans(table,b64_table)))
    else:
        value = bytes(value, 'utf-8')
        return b64decode(value)

def base64encode(value,table=None):
    b64_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    value = bytes(value,'utf-8')
    if table:
        return str(str.translate(str(b64encode(value)),str.maketrans(b64_table,table)))[2:-1]
    else:
        return b64encode(value)

def base64pickle(value):
    retVal = None
    try:
        retVal = b64encode(pickle.dumps(value, pickle.HIGHEST_PROTOCOL))
    except:
        warnMsg = "problem occurred while serializing "
        warnMsg += "instance of a type '%s'" % type(value)
        single_time_warn_message(warnMsg)
        try:
            retVal = b64encode(pickle.dumps(value))
        except:
            retVal = b64encode(pickle.dumps(str(value), pickle.HIGHEST_PROTOCOL))
    return retVal

def base64unpickle(value, unsafe=False):

    def loads(str):
        return pickle.loads(str)

    try:
        retVal = loads(b64decode(value))
    except TypeError:
        retVal = loads(b64decode(bytes(value)))

    return retVal

def AESEncode(message,key,iv):
    obj = AES.new(key, AES.MODE_CBC,iv)
    return obj.encrypt(message)

def AESDecode(ciphertext,key,iv):
    obj = AES.new(key, AES.MODE_CBC,iv)
    return obj.decrypt(ciphertext)

def CaesarEncode(plaintext, shift=3):
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = string.maketrans(alphabet, shifted_alphabet)
    return plaintext.translate(table)

def CaesardDecode(ciphertext, shift=3):
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[26-shift:] + alphabet[:26-shift]
    table = string.maketrans(alphabet, shifted_alphabet)
    return ciphertext.translate(table)


def DESEncode(ecryptText,key,iv):
    try:
        cipherX = DES.new(key,DES.MODE_CBC,iv)
        pad = 8 - len(ecryptText) % 8
        padStr = ""
        for i in range(pad):
            padStr = padStr + chr(pad)
        ecryptText = ecryptText + padStr
        x = cipherX.encrypt(ecryptText)
        return x.encode('hex_codec').upper()
    except:
        return ""


def DESDecode(decryptText,key,iv):
    try:

        cipherX = DES.new(key, DES.MODE_CBC, iv)
        str = decryptText.decode('hex_codec')
        y = cipherX.decrypt(str)
        return y[0:ord(y[len(y) - 1]) * -1]
    except:
        return ""

'''
    pBit=512 # set p bite
    qBit=512 # set q bite
    e=17 # set e
    ###########################################
    data="这是一个测试。1234567890abcdefghiABCDEF"
    rsa=RsaDemo(pBit,qBit,e)
    res = rsa.encode(data)
    print "#################public key#################"
    print "({0},{1})".format(rsa.e,rsa.n)
    print "#################private key################"
    print "({0},{1})".format(rsa.d, rsa.n)
    print "#################encode data################"
    print "({0})".format(res)
    print "#################decode data################"
    print "({0})".format(rsa.decode(res))
'''
class RsaDemo:
    def __init__(self,pBit,qBit,e):
        self.e = e
        while True:
            self.p=self.genP_Q(pBit)
            self.q=self.genP_Q(qBit)
            self.phi=(self.p-1)*(self.q-1)
            self.d=RSA.inverse(e,self.phi)
            if(self.d!=1):
                break
        self.n = self.p * self.q
    def encode_init(self,n,e):
        self.n = n
        self.e = e
    def genP_Q(self,bit):
        return number.getPrime(bit)
    def parseData(self,data):# change data to int
        return int(data.encode('hex'),16)
    def parseDataD(self, data):  # change int to string
        return hex(data)[2:].strip('L').decode('hex')
    def encode(self,data):
        data=self.parseData(data)
        return pow(data,self.e,self.n)
    def decode(self,encData):
        return self.parseDataD(pow(encData,self.d,self.n))




