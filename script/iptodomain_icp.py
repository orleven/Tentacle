#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'



def get_script_info(data=None):
    script_info = {
        "name": "iptodomain_icp",
        "info": "批量ip反查域名，域名查询备案信息。ip 反查调用接口：aizhan、chinaz、114best，域名ICP调用接口：aizhan、beianbeian、sobeian",
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    timeout = 3
    dic = _initdic(data['target_host'],data['id'])
    if dic['flag'] :

        dic = _byaizhan(data['target_host'],dic,headers,timeout)
        dic = _bychinaz(data['target_host'],dic,headers,timeout)
        dic = _by114best(data['target_host'],dic,headers,timeout)

        if not dic['flag']:
            dic['domain'] = "Curl Failed"
    else:
        dic['domain'].append(data['target_host'])
    if  len(dic['domain'])>0:
        for domain in dic['domain']:
            flag = False

            dic,myflag = _ICPsobeian(domain,dic,headers,timeout)
            flag |= myflag

            if not myflag :
                dic,myflag = _ICPbyaizhan(domain,dic,headers,timeout)
                flag |= myflag

            if not myflag :
                dic,myflag = _ICPbybeianbeian(domain,dic,headers,timeout)
                flag |= myflag

            # if not flag:
            #     dic['ICP'].append(domain)
    if len(dic['ICP'])>0:
        data['flag'] = True
        for _icp in dic['ICP']:
            data['res'].append({"info": _icp})
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
    import re
    temptext =  re.search(r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])(?:\.(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])){3}',target)
    if temptext != None:
        dic['domain'].append(target)
        dic['flag'] = True
    return dic

def _byaizhan(target, dic,headers, timeout=3):
    for j in range(3):
        try:
            url = "https://dns.aizhan.com/" + target.strip(' ') + "/"
            import requests
            from bs4 import BeautifulSoup
            result = requests.get(url, headers=headers, timeout=int(timeout))
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
    print("[-] Error for (%s)%s by aizhan" % (dic['id'], target))
    return dic


def _bychinaz(target, dic,headers, timeout=3):
    for j in range(3):
        try:
            import requests
            from bs4 import BeautifulSoup
            url = "http://s.tool.chinaz.com/same?s=" + target.strip(' ')
            result = requests.get(url, headers=headers, timeout=int(timeout))
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
    print("[-] Error for (%s)%s by chinaz" % (dic['id'], target))
    return dic


def _by114best(target, dic,headers, timeout=3):
    for j in range(3):
        try:
            import requests,random
            from bs4 import BeautifulSoup
            url = "http://www.114best.com/ip/114.aspx?w=" + target.strip(' ')
            headers['X-Forwarded-For'] = '.'.join(
                [str(random.randint(0, 255)), str(random.randint(0, 255)), str(random.randint(0, 255)),
                 str(random.randint(0, 255))])
            result = requests.get(url, headers=headers, timeout=int(timeout))
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
    print("[-] Error for (%s)%s by 114best" % (dic['id'], target))
    return dic


def _ICPsobeian(domain, dic, headers,timeout=3):
    flag = False
    for j in range(3):
        flag = False
        try:
            ICPinfo = domain
            ICPTime = "None"
            import requests,re
            from bs4 import BeautifulSoup
            url = "http://www.sobeian.com/search?key=" + domain.strip(' ') + "/"
            result = requests.get(url, headers=headers, timeout=int(timeout))
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
    print("[-] Error for ICP(%s)%s by sobeian" % (dic['id'], domain))
    return dic, flag


def _ICPbyaizhan(domain, dic, headers,timeout=3):
    flag = False
    for j in range(3):
        flag = False
        try:
            import requests
            from bs4 import BeautifulSoup
            url = "https://icp.aizhan.com/" + domain.strip(' ') + "/"
            result = requests.get(url, headers=headers, timeout=int(timeout))
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
    print("[-] Error for ICP(%s)%s by aizhan" % (dic['id'], domain))
    return dic, flag

def _ICPbybeianbeian(domain, dic, headers,timeout=3):
    flag = False
    for j in range(3):
        flag = False
        try:
            import requests,re
            from bs4 import BeautifulSoup
            url = "http://www.beianbeian.com/search/" + domain.strip(' ')
            result = requests.get(url, headers=headers, timeout=int(timeout))
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
    print("[-] Error for ICP(%s)%s by beianbeian" % (dic['id'], domain))
    return dic, flag
