# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# __author__ = 'orleven'
# import threading
# import requests
# import argparse
# import sys
# import os
# import platform
# import chardet
# from openpyxl import Workbook
# from bs4 import BeautifulSoup
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
#
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# type = sys.getfilesystemencoding()
# '''
#     批量检测目标是否属于Web应用，并检测关键词，以及得到http请求方法
#     Usage:
#         python curl.py -K title -T 3 -F file.txt
#         python curl.py -K status -F file.txt
#         python curl.py -F file.txt -V
#         python curl.py -F file.txt -S admin,管理,后台 -N 100 -V
#     目标格式:
#         http://www.baidu.com
#         http://192.168.1.11
#         http://192.168.1.22:80
#         www.baidu.com
#         127.0.0.1
# '''
#
# # targetList = [ ]
# # resultDic = {}
# thread_list = []
# search_list = []
# # resultList = []
# table_title_list = []
# queue = queue.Queue()
# file_lock = threading.Lock()
# load_lock = threading.Lock()
# codes = ['gbk', 'utf-8']
# book = Workbook()
# ws = book.active
# x = 1
# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
# }
#
#
# def curl_head(target, headers, timeout=3):
#     try:
#         requests.head(target, headers=headers, verify=False, timeout=timeout)
#         return target
#     except:
#         pass
#     return None
#
#
# def get_base_url(url):
#     protocol, s1 = urllib.parse.splittype(url)
#     host, s2 = urllib.parse.splithost(s1)
#     host, port = urllib.parse.splitport(host)
#     port = port if port != None else 443 if protocol == 'https' else 80
#     base_url = protocol + "://" + host + ":" + str(port)
#     return base_url, host, port
#
#
# def curl(timeout=3):
#     load_lock.acquire()
#     i, target = queue.get(timeout=1.0)
#     load_lock.release()
#     dic = {}
#     dic['id'] = str(i)
#     dic['search'] = []
#     dic['title'] = "[Curl Failed]"
#     dic['status'] = "0"
#     dic['flag'] = False
#     dic['host'] = target.strip().split(':')[0].strip('https://').strip('http://')
#     dic['target'] = target.strip()
#     if target.startswith('http://') or target.startswith('https://'):
#         base_url, host, port = get_base_url(target)
#     else:
#         for pro in ['http://', "https://"]:
#             url = curl_head(pro + target, headers)
#             if url:
#                 base_url, host, port = get_base_url(url)
#                 break
#     dic['host'] = host
#     dic['port'] = port
#     if url:
#         dic['target'] = url
#
#     try:
#         result = requests.get(url, timeout=int(timeout), verify=False)
#         soup = BeautifulSoup(result.text)
#         dic['status'] = str(result.status_code)
#         dic['flag'] = True
#         title = soup.title.string
#         if title == None or title == '':
#             title = "[None Title]".encode('utf-8')
#         else:
#             title = title.encode(result.encoding)
#
#         content = result.text
#         for searchkey in search_list:
#             if searchkey in title.encode(result.encoding).decode('utf-8').encode(type) or searchkey in content.encode(
#                     result.encoding).decode('utf-8').encode(type):
#                 # print searchkey,title.encode(result.encoding).decode('utf-8').encode(type)
#                 dic['search'].append(searchkey)
#
#         codes.append(result.encoding)
#         for j in range(0, len(codes)):
#             try:
#                 dic['title'] = title.decode(codes[j]).strip().replace("\r", "").replace("\n", "")
#                 break
#             except:
#                 pass
#             finally:
#                 if j + 1 == len(codes):
#                     dic['title'] = ['Error Code']
#
#     try:
#         result = requests.options(base_url + "/testbyah", timeout=int(timeout))
#         dic['head_allow'] = result.headers['Allow']
#     except:
#         dic['head_allow'] = "[Not Allow]"
#
#     file_lock.acquire()
#     print
#     "[%s]\t[%s]\t%s\t%s" % (str(i), dic['status'], dic['target'], dic['head_allow']
#     file_lock.release()
#     return dic
#
#
# def scan(thread_num, timeout, search_list):
#     print
#     "[.] Run start: Total " + str(queue.qsize()) + " request!"
#     for threadId in xrange(0, thread_num):
#         t = threading.Thread(target=curl, args=(timeout,))
#         t.start()
#         thread_list.append(t)
#     for num in xrange(0, thread_num):
#         thread_list[num].join()
#     print
#     "\r\n[.] Run over!"
#
#
# def argSet(parser):
#     # parser.add_argument("-K", "--key", type=str, help="The order key e.g. title、status、host", default="id")
#     parser.add_argument("-T", "--timeout", type=str, help="Timeout", default="3")
#     parser.add_argument("-F", "--file", type=str, help="Load ip dictionary e.g. 192.168.1.2:8080", default=None)
#     # parser.add_argument("-V", "--verbose",action='store_true',help="verbose", default=False)
#     parser.add_argument("-O", "--out", type=str, help="output file e.g res.txt", default=None)
#     parser.add_argument("-S", "--search", type=str, help="search key in title or content,e.g. 管理,后台", default=None)
#     parser.add_argument("-N", "--threadnum", type=int, help="Thread Num e.g. 10", default=10)
#     return parser
#
#
# def handle(args):
#     timeout = args.timeout
#     filename = args.file
#     out = args.out
#     threadnum = args.threadnum
#     search = args.search
#     search_list = []
#     if search != None:
#         search_list = search.split(',')
#     if filename != None:
#         if os.path.isfile(filename):
#             with open(filename, 'r') as f:
#                 for line in f.readlines():
#                     myline = line.strip('\n').strip('\r')
#                     queue.put(myline)
#         else:
#             print
#             "[-] The path is not exist!"
#     scan(threadnum, timeout, search_list)
#
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
#     parser = argSet(parser)
#     args = parser.parse_args()
#     handle(args)
