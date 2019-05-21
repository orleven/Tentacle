#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import os
import queue
import time
import sys
import socks
import socket
import traceback
import threading
import importlib.util
from lib.core.common import get_safe_ex_string
from lib.core.database import TaskDataDB
from lib.core.data import conf, logger,paths
from lib.utils.output import print_dic
from lib.utils.output import output_excal
from lib.core.common import unserialize_object
from lib.utils.iputil import build
from lib.utils.iputil import check_host
from lib.utils.iputil import check_ippool
from lib.api.api import search_engine
from lib.api.api import search_api

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
        self.parameter = None
        self.func_name = 'prove'
        self.put_queue_flag = True
        self.thread_count = self.thread_num  = conf['thread_num']
        self.scanning_count = self.scan_count = self.found_count = self.error_count = self.total = self.exclude =0
        self.is_continue = True
        self.queue_pool_total = 3000
        self.queue_pool_cache = 1000
        self.target_pool_total = 65535 * 255
        self.start_time =  self.current_time = time.time()
        self.set_thread_lock()
        self.hashdb = TaskDataDB(os.path.join(paths.DATA_PATH,name))
        self.hashdb.connect()
        self.hashdb.init()
        logger.debug("Engine inited.")


    def _load_module(self,module_name, func_name):
        module_spec = importlib.util.find_spec(module_name)
        module = None
        if module_spec:
            try:
                module = importlib.import_module(module_name)

                if 'POC' not in dir(module):
                    logger.error('Invalid POC script, Please check the script: %s' % module.__name__)
                    return None

                self.modules.append(module)
            except:
                logger.error('Invalid POC script, Please check the script: %s' % module_name)
                return None
        else:
            logger.error('Can\'t load modual: %s.' % conf.module_path)
            return None

        return module

    def load_modules(self):
        modules_name = conf['modules_name']
        func_name = conf['func_name']

        if len(modules_name) < 0:
            msg = 'Can\'t find any modules. Please check you input.'
            sys.exit(logger.error(msg))

        elif len(modules_name) == 1:
            logger.sysinfo('Loading modual: %s' % (modules_name[0]))
            module = self._load_module(modules_name[0], func_name)

            if func_name.lower() in ['show','help'] and module:
                poc = module.POC()
                msg = "Show POC's Infomation:"
                msg += "\r\n ------------------------------- "
                msg += "\r\n| Name: " + str(poc.name if 'name' in poc.__dict__ else 'unknown')
                msg += "\r\n| Keyword: " + str(poc.keyword if 'keyword' in poc.__dict__ else ['unknown'])
                msg += "\r\n| Infomation: " + str(poc.info if 'info' in poc.__dict__ else 'Unknown POC, please set the infomation for me.')
                msg += "\r\n| Level: " + str(poc.level if 'level' in poc.__dict__ else 'unknown')
                msg += "\r\n| Refer: " + str(poc.refer if 'refer' in poc.__dict__ else None)
                msg += "\r\n| Type: " + str(poc.type if 'type' in poc.__dict__ else 'unknown')
                msg += "\r\n| Repaire: " + str(poc.repaire if 'repaire' in poc.__dict__ else 'unknown')
                msg += "\r\n| Default Port: " + str(poc.server_type if 'server_type' in poc.__dict__ else 'unknown')
                msg += "\r\n ------------------------------- "
                logger.sysinfo(msg)
                sys.exit()

        else:
            logger.sysinfo('Loading moduals...')
            for module_name in conf['modules_name']:
                module = self._load_module(module_name, func_name)

                if len(self.modules) > 1 and func_name.lower() in  ['show','help']:
                    sys.exit(logger.error('Can\'t show so many modules.'))

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
                target = target[:-1] if target[-1] == '/' else target
                if ":" in target:
                    _v = target.split(':')
                    host = _v[0]
                    if check_host(host):
                        self.put_target(target,service)
                else:
                    if check_host(target):
                        self.put_target(target,service)

    def load_parameter(self):
        if 'parameter' in conf.keys() and conf['parameter'] != None:
            try:
                datas = conf['parameter'].split('&')
                dic = {}
                for _data in datas:
                    _key, _value = _data.split('=')
                    dic[_key] = _value
                self.parameter = dic
                logger.sysinfo("Loading parameter: %s" % (conf['parameter']))
            except:
                msg = 'The parameter input error, please check your input e.g. -p "userlist=user.txt", and you should make sure the module\'s function need the parameter. '
                sys.exit(logger.error(msg))
        else:
            self.parameter = {}

    def load_config(self):
        if conf['config']['proxy']['proxy'].lower() == 'true':
            try:
                socks5_host, socks5_port = conf['config']['proxy']['socks5'].split(':')
                socks.setdefaultproxy(socks.SOCKS5, socks5_host, int(socks5_port))
                socket.socket = socks.socksocket
            except Exception as e:
                logger.error("Error socket proxy: %s" % conf['config']['proxy']['socks5'])
            logger.sysinfo("Set proxy: %s" % (conf['config']['proxy']['socks5']))
        logger.sysinfo("Set timeout: %s" % (conf['config']['basic']['timeout']))
        socket.setdefaulttimeout(int(conf['config']['basic']['timeout']))

    def load_function(self):
        self.func_name = conf['func_name']
        logger.sysinfo("Loading function: %s" % (conf['func_name']))

    def load_targets(self):

        if 'target_simple' in conf.keys():
            self._load_target(conf['target_simple'])
            logger.sysinfo("Loading target: %s" % (conf['target_simple']))

        elif 'target_file' in conf.keys():
            with open(conf['target_file'], 'r') as f:
                for _line in f.readlines():
                    line = _line.replace("\r","").replace("\n","").strip()
                    if line and line != '':
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
            hashdb = TaskDataDB(os.path.join(paths.DATA_PATH,conf['target_task']))
            hashdb.connect()
            for _row in hashdb.select_all():
                if _row[5] != None and _row[5] != '':
                    self._load_target(_row[5])
                else:
                    self._load_target(_row[3] + ":" + _row[4])
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
                poc = module.POC(obj)
                for target, port in poc.get_target_port_list():
                    obj = ':'.join([poc.target_host,str(port)])
                    self.total += 1
                    # if service !=None and service.lower() not in ['','unknown'] and service.lower() not in module.__name__.lower():
                    #     self.exclude += 1
                    #     continue
                    if target:
                        if target.startswith('http://') or target.startswith('https://'):
                            self.queue.put([i + 1, module, target])
                        else:
                            self.queue.put([i + 1, module, obj])
                    else:
                        self.queue.put([i + 1, module, obj])

                    if self.queue.qsize() >= self.queue_pool_total + self.queue_pool_cache :
                        yield self.queue
        yield self.queue


    def _get_data(self):
        if conf.OUT != None:
            logger.sysinfo('[%s] Task sort out the data. ' % self.name)
            datas = []
            for _row in self.hashdb.select_all():
                data = {
                    "id": _row[0],
                    "tid": _row[1],
                    "flag": _row[2],
                    'target_host': _row[3],
                    'target_port': _row[4],
                    'url': _row[5],
                    'module_name': _row[6],
                    "req":  unserialize_object(_row[7]),
                    "res": unserialize_object(_row[8]),
                    "other": unserialize_object(_row[9])
                }
                datas.append(data)
            output_excal(datas, conf.OUT, self.name)

    def run(self):
        logger.sysinfo('Task running: %s', self.name)
        pool = self._put_queue()
        next(pool)
        self.print_progress()

        # add
        # thread_pool = ThreadPoolExecutor(max_workers=self.thread_num)
        # for i in range(0, self.thread_num):
        #     future = thread_pool.submit(self._work)

        logger.debug("Wait for thread...")

        for i in range(0, self.thread_num):
            t = threading.Thread(target=self._work, name=str(i))
            self.set_thread_daemon(t)
            t.start()

        while True:
            if self.thread_count > 0 and self.is_continue:
                now_time = time.time()
                if now_time - self.current_time >= 60:
                    self.current_time = now_time
                    self.print_progress()

                if self.put_queue_flag and self.queue.qsize() < self.queue_pool_total:
                    try:
                        next(pool)
                        logger.debug("Add queue pool for engine.")
                    except StopIteration:
                        self.put_queue_flag = False

                time.sleep(0.01)
                # try:
                #     time.sleep(0.01)
                # except KeyboardInterrupt:
                #     self.is_continue = False
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

                if not self.is_continue:
                    break

                # Wait for pool
                if self.total > self.queue_pool_total + self.queue_pool_cache :
                    time.sleep(3)

                if self.queue.qsize() <= 0 and self.scan_count == self.total :
                    break
                else:
                    continue

        self.change_thread_count(-1)

    def _scan(self,id,module,target):
        try:
            poc = module.POC(target)
            func = getattr(poc, self.func_name)
            # for port in poc.get_target_port_list():
            logger.debug("Running %s:%s for %s:%s" % (module.__name__, self.func_name, poc.target_host, poc.target_port))
            poc.re_initialize(target, poc.target_host, poc.target_port, self.parameter)
            func()
            # logger.warning("OVER %s" %module.__name__)
            if conf.VERBOSE or poc.flag != -1:
                if poc.flag == 1:
                    self.change_found_count(1)
                data = {
                    "id": id,
                    "flag": poc.flag,
                    'module_name': module.__name__,
                    'func_name': self.func_name,
                    'target_host': poc.target_host,
                    'target_port': poc.target_port,
                    'url': poc.url,
                    'base_url': poc.base_url,
                    "req": poc.req,
                    "res": poc.res,
                    "other": poc.other,
                }
                self.hashdb.insert(data)
                self.hashdb.flush()
                print_dic(data)

        except AttributeError as e:
            if 'has no attribute \'POC\'' in get_safe_ex_string(e):
                logger.error('Invalid POC script, Please check the script: %s' %module.__name__,)
            elif '\'POC\' object has no attribute' in get_safe_ex_string(e):
                logger.error('Attribute is not exist, Please check \'%s\' in the script: %s' % (self. func_name, module.__name__,))
            elif 'Function is not exist.' in get_safe_ex_string(e):
                logger.error('Function is not exist, Please check \'%s\' in the script: %s' % (self. func_name, module.__name__,))
            else:
                logger.error("%s %s:%s for %s" % (e, module.__name__, self.func_name, target))
            self.change_error_count(1)
        except KeyError as e:
            logger.error("Missing parameters: %s, please load parameters by -p. For example. -p %s=value" % (e,str(e).replace('\'','')))
        except Exception as e:
            self.errmsg = traceback.format_exc()
            self.is_continue = False
            logger.error(self.errmsg)

    def print_progress(self):
        # self.total = len(self.targets) * len(self.modules) - self.exclude
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

    def change_found_count(self,num):
        self.found_count_lock.acquire()
        self.found_count += num
        self.found_count_lock.release()

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