#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re
import random
import requests
from bs4 import BeautifulSoup

def info(data=None):
    info = {
        "name": "iptodomain_icp",
        "info": "search domain: aizhan、chinaz、114best, search icp: aizhan、beianbeian、sobeian.",
        "level": "low",
        "type": "info",
    }
    return info



def prove(data):
    data = init(data, 'api')
    dic = _initdic(data['target_host'],data['id'])
    if dic['flag'] :
        dic = _byaizhan(data['target_host'],dic)
        dic = _bychinaz(data['target_host'],dic)
        dic = _by114best(data['target_host'],dic)
        if not dic['flag']:
            dic['domain'] = "Curl Failed"
    else:
        dic['domain'].append(data['target_host'])
    if  len(dic['domain'])>0:
        for domain in dic['domain']:
            flag = False
            dic,myflag = _ICPbybeianbeian(domain,dic)
            flag |= myflag

            if not myflag :
                dic,myflag = _ICPbyaizhan(domain,dic)
                flag |= myflag

            if not myflag :
                dic,myflag = _ICPsobeian(domain,dic)
                flag |= myflag

            # if not flag:
            #     dic['ICP'].append(domain)
    if len(dic['ICP'])>0:
        data['flag'] = 1
        for _icp in dic['ICP']:
            data['res'].append({"info": _icp.strip('\r'),"key": "icp"})
    return data


def _initdic(target,i):
    dic = {}
    dic['id'] = i
    dic['ip'] = target
    dic['chinaz_domain'] = False
    dic['114best_domain'] = False
    dic['aizhan_domain'] = False
    dic['beianbeian_icp'] = False
    dic['aizhan_icp'] = False
    dic['sobeian_icp'] = False
    dic['host'] = target
    dic['flag'] = False
    dic['domain'] = []
    dic['ICP']= []

    temptext =  re.search(r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])(?:\.(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])){3}',target)
    if temptext != None:
        dic['domain'].append(target)
        dic['flag'] = True
    return dic

def _byaizhan(target, dic):
    for j in range(3):
        try:
            url = "https://dns.aizhan.com/" + target.strip(' ') + "/"
            result = curl('get',url)
            soup = BeautifulSoup(result.text, "html5lib")
            alist = soup.find_all("td", class_="domain")
            for i in range(1, len(alist)):
                mydomain = alist[i].find("a").get_text()
                if mydomain not in dic['domain']:
                    dic['domain'].append(mydomain)
            dic['aizhan_domain'] = True
            dic['flag'] = True
            return dic
        except:
            pass
    logger.debug("Error for (%s)%s by aizhan" % (dic['id'], target))
    return dic


def _bychinaz(target, dic):
    for j in range(3):
        try:
            url = "http://s.tool.chinaz.com/same?s=" + target.strip(' ')
            result = curl('get', url)
            soup = BeautifulSoup(result.text, "html5lib")
            ul = soup.find(id="ResultListWrap")
            for div in soup.find_all("div", class_="w30-0 overhid"):
                mydomain = div.find("a").get_text()
                if mydomain not in dic['domain']:
                    dic['domain'].append(mydomain)
            dic['chinaz_domain'] = True
            dic['flag'] = True
            return dic
        except:
            pass
    logger.debug("Error for (%s)%s by chinaz" % (dic['id'], target))
    return dic


def _by114best(target, dic):
    for j in range(3):
        try:
            headers = {}
            url = "http://www.114best.com/ip/114.aspx?w=" + target.strip(' ')
            headers['X-Forwarded-For'] = '.'.join(
                [str(random.randint(0, 255)), str(random.randint(0, 255)), str(random.randint(0, 255)),
                 str(random.randint(0, 255))])
            result = curl('get', url)
            soup = BeautifulSoup(result.text, "html5lib")
            div = soup.find(id="rl")
            for span in div.find_all('span'):
                mydomain = span.get_text().replace(" ", "").replace("\r", "").replace("\n", "")

                if mydomain not in dic['domain']:
                    dic['domain'].append(mydomain)
            dic['114best_domain'] = True
            dic['flag'] = True
            return dic
        except:
            pass
    logger.debug("Error for (%s)%s by 114best" % (dic['id'], target))
    return dic


def _ICPsobeian(domain, dic):
    flag = False
    for j in range(3):
        flag = False
        try:
            ICPinfo = domain
            ICPTime = "None"
            url = "http://www.sobeian.com/search?key=" + domain.strip(' ') + "/"
            result = curl('get', url)
            soup = BeautifulSoup(result.text, "html5lib")
            for span in soup.find_all("span", class_="list-group-item clearfix"):
                alist = span.find_all('a', href=re.compile('/icp/details/'))
                if domain in alist[2].get_text().split(' '):
                    ICPinfo += ":" + alist[1].get_text()
                    temp = re.search(r'\d{4}\-\d{2}\-\d{2}', span.get_text())
                    if temp != None:
                        ICPTime = temp.group()
                    ICPinfo += ":" + ICPTime
                    dic['ICP'].append(ICPinfo)
                    flag = True
                    break
            dic['flag'] = True
            dic['sobeian_icp'] = True
            return dic, flag
        except:
            pass
    logger.debug("Error for ICP(%s)%s by sobeian" % (dic['id'], domain))
    return dic, flag


def _ICPbyaizhan(domain, dic):
    flag = False
    for j in range(3):
        flag = False
        try:
            url = "https://icp.aizhan.com/" + domain.strip(' ') + "/"
            result = curl('get', url)
            soup = BeautifulSoup(result.text, "html5lib")
            div = soup.find(id="icp-table")
            ICPinfo = domain
            if div != None:
                for span in div.find_all('span'):
                    info = span.get_text()
                    if info != None:
                        ICPinfo += ":" + info
            if ICPinfo != domain and ICPinfo not in dic['ICP']:
                dic['ICP'].append(ICPinfo)
                flag = True
            dic['flag'] = True
            dic['aizhan_icp'] = True
            return dic, flag
        except:
            pass
    logger.debug("Error for ICP(%s)%s by aizhan" % (dic['id'], domain))
    return dic, flag

def _ICPbybeianbeian(domain, dic):
    flag = False
    for j in range(3):
        flag = False
        try:
            url = "http://www.beianbeian.com/search/" + domain.strip(' ')
            result = curl('get', url)
            soup = BeautifulSoup(result.text, "html5lib")
            info1 = info2 = None
            alist = soup.find_all('a', href=re.compile('/beianxinxi/'))
            if len(alist) > 0:
                info1 = alist[0].get_text()
                div = soup.find(id="pass_time")
                info2 = div.get_text()
            ICPinfo = domain
            if info1 != None and info2 != None:
                ICPinfo += ":" + info1 + ":" + info2
            if ICPinfo != domain and ICPinfo not in dic['ICP']:
                dic['ICP'].append(ICPinfo)
                flag = True
            dic['flag'] = True
            dic['beianbeian_icp'] = True

            return dic, flag
        except:
            pass
    logger.debug("Error for ICP(%s)%s by beianbeian" % (dic['id'], domain))
    return dic, flag
