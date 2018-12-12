#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import queue
import time
import random
import sys
import urllib.parse
import re,os
import traceback
import threading
import importlib.util

from lib.core.hashdb import HashDB
from lib.core.data import conf, logger,paths
from lib.utils.output import print_dic
from lib.utils.cipher import md5
from lib.utils.output import output_excal
from lib.core.common import unserialize_object
from lib.utils.iputil import build
from lib.utils.iputil import check_host
from lib.utils.iputil import check_ip
from lib.utils.iputil import check_ippool
from lib.api.search import search_engine
from lib.api.search import search_api
from script import init
from script import curl

class Engine():

    def __del__(self):
        self.hashdb.disconnect()
        logger.debug("Task over: %s" %self.name )

    def __init__(self,name):
        logger.sysinfo("Task created: %s",name)
        self.name = name
        self.queue = queue.Queue()
        self.targets = []
        self.modules = []
        self.put_queue_flag = True
        self.thread_count = self.thread_num  = conf['thread_num']
        self.scanning_count = self.scan_count = self.found_count = self.error_count = self.total = self.exclude =0
        self.is_continue = True
        self.queue_pool_total = 3000
        self.queue_pool_cache = 1000
        self.target_pool_total = 65535 * 255
        self.start_time =  self.current_time = time.time()
        self.set_thread_lock()
        self.hashdb = HashDB(os.path.join(paths.DATA_PATH,name))
        self.hashdb.connect(name)
        self.hashdb.init()
        logger.debug("Engine inited.")


    def _load_module(self,module_name):
        module_spec = importlib.util.find_spec(module_name)
        if module_spec:
            module = importlib.import_module(module_name)
            self.modules.append(module)
        else:
            module = None
            logger.error('Can\'t load modual: %s.' % conf.module_path)
        return module


    def load_modules(self):
        modules_name = conf['modules_name']
        func_name = conf['func_name']

        if len(modules_name) < 0:
            msg = 'Can\'t find any modules. Please check you input.'
            sys.exit(logger.error(msg))

        elif len(modules_name) == 1:
            logger.sysinfo('Loading modual: %s.' % (modules_name[0]))
            module = self._load_module(modules_name[0])
            if func_name.lower() in ['show','help'] and module:
                sys.exit(help(module))

        else:
            logger.sysinfo('Loading moduals...')
            for module_name in conf['modules_name']:
                module = self._load_module(module_name)

                if len(self.modules) > 1 and func_name.lower() == 'show':
                    sys.exit(logger.error('Can\'t show so many modules.'))

                elif func_name not in dir(module):
                    logger.error('Can\'t find function: %s:%s(), please make sure the function is in the module.' % (module.__name__, func_name))

    def _load_target(self,target,service=None):

        # http://localhost
        if "http://" in target or "https://" in target:
            self.put_target(target,service)
        else:

            # 192.168.111.1/24
            if '/' in target and check_ippool(target):
                for each in build(target):
                    self.put_target(each,service)

            # 192.168.111.1-192.168.111.3
            elif '-' in target and check_ippool(target):
                _v = target.split('-')
                for each in build(_v[0], _v[1]):
                    self.put_target(each,service)

            # 192.168.111.1
            else:
                if ":" in target:
                    _v = target.split(':')
                    host = _v[0]
                    if check_host(host):
                        self.put_target(target,service)
                else:
                    if check_host(target):
                        self.put_target(target,service)


    def load_targets(self):

        if 'target_simple' in conf.keys():
            self._load_target(conf['target_simple'])
            logger.sysinfo("Loading target: %s" % (conf['target_simple']))

        elif 'target_file' in conf.keys():
            for _line in open(conf['target_file'], 'r'):
                line = _line.strip()
                if line:
                    self._load_target(line)
            logger.sysinfo("Loading target: %s" % (conf['target_file']))

        elif 'target_nmap_xml' in conf.keys():
            import xml.etree.ElementTree as ET
            tree = ET.parse(conf['target_nmap_xml'])
            root = tree.getroot()
            for host in root.findall('host'):
                host_id = host.find('address').get('addr')
                # infoLit = []
                for port in host.iter('port'):
                    port_id = port.attrib.get('portid')
                    port_protocol = port.attrib.get('protocol')
                    port_state = port.find('state').attrib.get('state')
                    try:
                        port_service = port.find('service').attrib.get('name')
                    except:
                        port_service = "None"
                    # infoDic = {"port": port_id, "status": port_state, "server": port_service, "other": port_protocol}
                    # infoLit.append(infoDic)
                    if port_state.lower() not in ['closed','filtered']:
                        self._load_target(host_id+":"+port_id,port_service)
                # resDic = {"host": host_id, "info": infoLit}
                # resLit.append(resDic)
            logger.sysinfo("Loading target: %s" % (conf['target_nmap_xml']))

        elif 'target_network' in conf.keys():
            self._load_target(conf['target_network'])
            logger.sysinfo("Loading target: %s" % (conf['target_network']))

        elif 'target_task' in conf.keys():
            hashdb = HashDB(os.path.join(paths.DATA_PATH,conf['target_task']))
            hashdb.connect()
            for _row in hashdb.select_all():
                if _row[4] != None and _row[4] != '':
                    self._load_target(_row[4])
                else:
                    self._load_target(_row[2] + ":" + _row[3])
            logger.sysinfo("Loading target: %s" % (conf['target_task']))

        elif 'target_search_engine' in conf.keys():
            logger.sysinfo("Loading target by baidu/bing/360so: %s" % (conf['target_search_engine']))
            urls = search_engine(conf['target_search_engine'])
            for _url in urls:
                if _url:
                    self._load_target(_url)

        elif 'target_zoomeye' in conf.keys():
            logger.sysinfo("Loading target by zoomeye: %s" % (conf['target_zoomeye']))
            urls = search_api(conf['target_zoomeye'])
            for _url in urls:
                if _url:
                    self._load_target(_url)

        elif 'target_shodan' in conf.keys():
            logger.sysinfo("Loading target by shadon: %s" % (conf['target_shodan']))
            urls = search_api(conf['target_shodan'])
            for _url in urls:
                if _url:
                    self._load_target(_url)

        elif 'target_fofa' in conf.keys():
            logger.sysinfo("Loading target by fofa: %s" % (conf['target_fofa']))
            urls = search_api(conf['target_fofa'])
            for _url in urls:
                if _url:
                    self._load_target(_url)

        elif 'target_fofa_today_poc' in conf.keys():
            logger.sysinfo("Loading target by fofa today poc: %s" % (conf['target_fofa_today_poc']))
            obj = search_api(conf['target_fofa_today_poc'])
            for _url,_server in obj:
                if _url:
                    self._load_target(_url,_server)

        elif 'target_google' in conf.keys():
            logger.sysinfo("Loading target by google: %s" % (conf['target_google']))
            urls = search_api(conf['target_google'])
            for _url in urls:
                if _url:
                    self._load_target(_url)

        elif 'target_github' in conf.keys():
            logger.sysinfo("Loading target by github: %s" %(conf['target_github']))
            urls = search_api(conf['target_github'])

        else:
            sys.exit(logger.error("Can't load any targets! Please check input." ))

        if len(self.targets) == 0:
            sys.exit(logger.error("Can't load any targets! Please check input."))

    def set_thread_daemon(self,thread):
        thread.setDaemon(True)

    def put_target(self,obj,service = None):
        self.targets.append([obj, service])
        if len(self.targets) > self.target_pool_total:
            msg = 'Too many targets! Please control the target\'s numbers under the %d.' % self.target_pool_total
            sys.exit(logger.error(msg))

    def _put_queue(self):
        for module in self.modules:
            for i in range(0,len(self.targets)):
                obj, service = self.targets[i]
                if service !=None and service.lower() not in ['','unknown'] and service.lower() not in module.__name__:
                    self.exclude += 1
                    continue

                self.queue.put([i+1,module,obj])
                if self.queue.qsize() >= self.queue_pool_total + self.queue_pool_cache:
                    yield self.queue
        yield self.queue


    def _get_data(self):
        if conf.OUT != None:
            logger.info('(%s) Task sort out the data. ' % self.name)
            datas = []
            for _row in self.hashdb.select_all():
                data = {
                    "id": _row[0],
                    "flag": _row[1],
                    'target_host': _row[2],
                    'target_port': _row[3],
                    'url': _row[4],
                    "data": unserialize_object(_row[5]),
                    "res": unserialize_object(_row[6]),
                    "other": unserialize_object(_row[7])
                }
                datas.append(data)
            output_excal(datas, conf.OUT, self.name)

    def run(self):
        logger.sysinfo('Task running: %s', self.name)
        pool = self._put_queue()
        next(pool)

        self.print_progress()
        for i in range(0, self.thread_num):
            t = threading.Thread(target=self._work, name=str(i))
            self.set_thread_daemon(t)
            t.start()

        logger.debug("Wait for thread...")

        while True:
            if self.thread_count > 0 and self.is_continue:
                now_time = time.time()
                if now_time - self.current_time >= 60:
                    self.current_time = now_time
                    self.print_progress()

                if  self.put_queue_flag and self.queue.qsize() < self.queue_pool_total :
                    try:
                        next(pool)
                        logger.debug("Add queue pool for engine.")
                    except StopIteration:
                        self.put_queue_flag = False

                time.sleep(0.01)

            else:
                self.print_progress()
                self._get_data()
                break
        logger.sysinfo('Task Finished: %s', self.name)

    def _work(self):
        while True:
            self.load_lock.acquire()
            if self.queue.qsize() > 0 and self.is_continue:
                id,module,target = self.queue.get(timeout=1.0)
                self.load_lock.release()
                self.change_scanning_count(+1)
                self._scan(id, module, target)
                self.change_scanning_count(-1)
                self.change_scan_count(1)
            else:
                self.load_lock.release()

                # Wait for pool
                if self.total > self.queue_pool_total + self.queue_pool_cache :
                    time.sleep(3)

                if self.queue.qsize() <= 0 and self.scan_count == self.total :
                    break
                else:
                    continue


        self.change_thread_count(-1)

    def _scan(self,id,module,target):
        data = self._init_data(id,module,target)

        try:
            logger.debug("Test %s:%s for %s:%s" % (
            data['module_name'], conf['func_name'], data['target_host'], data['target_port']))
            func = getattr(module, conf['func_name'])
            module.init = init
            module.curl = curl
            module.logger = logger
            data = func(data)
            if conf.VERBOSE or data['flag'] == 1:
                if data['flag'] == 1:
                    self.found_count += 1
                self.hashdb.insert(data)
                self.hashdb.flush()
                print_dic(data)
        except AttributeError:
            self.change_error_count(1)
        except Exception:
            self.errmsg = traceback.format_exc()
            self.is_continue = False
            logger.error(self.errmsg)
        pass

    def _init_data(self,id,module,target):

        # 未来替换为这个
        # data = {
        #     "id": id,
        #     'module_name': module.__name__ ,
        #     'func_name': conf['func_name'],
        #     "flag": -1,
        #      "service": None,
        #     'target_host': None,
        #     'target_port': None,
        #     'url': None,
        #     'base_url': None,
        #     'headers': {},
        #
        #     "data": [],  # Send
        #     "res": [],  # Rec
        # }

        data = {
            "id": id,
            "flag": -1,
            "service": None,
            'target_host': None,
            'target_port': None,
            'url': None,
            'base_url': None,
            'module_name': module.__name__,
            'func_name': conf['func_name'],
            "data": [],
            "res": [],
            "other": {},
            'headers': {},
        }

        if target.startswith('http://') or target.startswith('https://'):
            data['url'] = target
            protocol, s1 = urllib.parse.splittype(target)
            host, s2 = urllib.parse.splithost(s1)
            host, port = urllib.parse.splitport(host)
            data['target_host'] = host
            data['target_port'] = port if port != None else 443 if protocol == 'https' else 80
            data['base_url'] = protocol + "://" + host + ":" + str(data['target_port']) + '/'
            data['service'] = "http" if protocol == 'http' else "https"
        else:
            if ":" in target:
                _v = target.split(':')
                host, port = _v[0], _v[1]
                data['target_host'] = host
            else:
                port = 0
                data['target_host'] = target
            data['target_port'] = conf['target_port'] if 'target_port' in conf.keys() else int(port)

        return data


    def print_progress(self):
        self.total = len(self.targets) * len(self.modules) - self.exclude
        msg = '[%s] %s found | %s error | %s remaining | %s scanning | %s scanned in %.2f seconds.(total %s)' % (
            self.name, self.found_count, self.error_count, self.queue.qsize(),  self.scanning_count, self.scan_count, time.time() - self.start_time,self.total)
        logger.sysinfo(msg)

    def set_thread_lock(self):
        self.found_count_lock = threading.Lock()
        self.scan_count_lock = threading.Lock()
        self.thread_count_lock = threading.Lock()
        self.file_lock = threading.Lock()
        self.load_lock = threading.Lock()
        self.error_count_lock = threading.Lock()
        self.scanning_count_lock = threading.Lock()

    def change_thread_count(self,num):
        self.thread_count_lock.acquire()
        self.thread_count += num
        self.thread_count_lock.release()

    def change_scan_count(self,num):
        self.scan_count_lock.acquire()
        self.scan_count += num
        self.scan_count_lock.release()

    def change_scanning_count(self,num):
        self.scanning_count_lock.acquire()
        self.scanning_count += num
        self.scanning_count_lock.release()

    def change_error_count(self, num):
        self.error_count_lock.acquire()
        self.error_count += num
        self.error_count_lock.release()