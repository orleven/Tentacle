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
from lib.core.enums import SERVICE_PORT_MAP
from lib.core.enums import SERVICE_NOT_WEB_LIST
import urllib.parse
import xml.etree.ElementTree as ET
from lib.core.common import get_safe_ex_string
from lib.core.database import TaskDataDB
from lib.core.data import conf, logger,paths
from lib.utils.output import print_dic
from lib.utils.output import output_excal
from lib.core.common import unserialize_object
from lib.utils.iputil import build
from lib.utils.iputil import check_ippool
from lib.api.api import search_engine
from lib.api.api import search_api

class Engine():

    def __del__(self):
        self.hashdb.disconnect()
        logger.sysinfo("Task over: %s" %self.name )

    def __init__(self, name):
        self.name = name

        self.modules = []

        # targets = {
        #     "127.0.0.1": {
        #         '80': ('web', None),
        #         '3389': ('rdp', None),
        #     },
        #     "www.baidu.com": {
        #         '80': [('web', 'http://www.baidu.com'),('web','http://www.baidu.com/aaaa')],
        #         '3389': ('rdp', None),
        #     },
        # }
        self.targets = {}
        self.parameter = None
        self.func_name = 'prove'
        self.is_continue = True
        self.queue = queue.Queue()
        self.pools = []
        self.queue_pool_total = 1024
        self.queue_pool_cache = 16
        self.target_pool_total = 65535 * 10
        self.scanning_count = self.scan_count = self.found_count = self.error_count = self.total = self.exclude = 0
        self.thread_count = self.thread_num  = conf['thread_num']
        self.start_time =  self.current_time = time.time()
        self.set_thread_lock()
        self.hashdb = TaskDataDB(os.path.join(paths.DATA_PATH, name))
        self.hashdb.connect()
        self.hashdb.init()
        logger.sysinfo("Task created: %s", name)

    def run(self):
        logger.sysinfo('Task running: %s', self.name)

        pool = self.put_queue()
        next(pool)
        self.pools.append(pool)
        self.print_progress()

        logger.debug("Wait for thread...")

        for i in range(0, self.thread_num):
            t = threading.Thread(target=self.worker, name=str(i))
            self.set_thread_daemon(t)
            t.start()

        while True:
            if self.thread_count > 0 and self.is_continue:
                now_time = time.time()
                if now_time - self.current_time >= 60:
                    self.current_time = now_time
                    self.print_progress()

                if len(self.pools) > 0 and self.queue.qsize() < self.queue_pool_cache:
                    for pool in self.pools:
                        try:
                            if self.queue_pool_cache < self.queue_pool_total:
                                self.queue_pool_cache *= 2
                            next(pool)
                            logger.debug("Add queue pool for engine.")
                            break
                        except StopIteration:
                            self.pools.remove(pool)

                time.sleep(0.01)

            else:
                self.print_progress()
                self.get_data()
                break

        logger.sysinfo('Task Finished: %s', self.name)

    def worker(self):
        while True:
            self.load_lock.acquire()
            if self.queue.qsize() > 0 and self.is_continue:
                id,module,obj = self.queue.get(timeout=1.0)
                self.load_lock.release()
                self.change_scanning_count(+1)
                self.scan(id, module, obj)
                self.change_scanning_count(-1)
                self.change_scan_count(1)
            else:
                self.load_lock.release()

                if not self.is_continue:
                    break

                # Wait for pool
                if self.total > self.queue_pool_cache :
                    time.sleep(3)

                if self.queue.qsize() <= 0 and self.scan_count == self.total :
                    break
                else:
                    continue

        self.change_thread_count(-1)

    def scan(self,id,module,obj):
        host, port, service, url = obj
        try:
            poc = module.POC()
            poc.initialize(host, port, url, self.parameter)
            func = getattr(poc, self.func_name)
            logger.debug("Running %s:%s for %s:%s" % (module.__name__, self.func_name, poc.target_host, poc.target_port))
            func()
            if conf.VERBOSE or poc.flag >=0 :
                if poc.flag >= 1:
                    self.change_found_count(1)
                    if poc.flag == 2:
                        if not conf['noportscan'] or module.__name__ != 'script.info.port_scan':
                            url = poc.url if poc.url != None else poc.base_url if poc.base_url !=None else None
                            service = poc.service_type[0]
                            pool = self.put_queue_by_res(id, module, host, port, service, url)
                            self.pools.append(pool)
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
                logger.error('Invalid POC script, Please check the script: %s' % module.__name__, )
            elif '\'POC\' object has no attribute' in get_safe_ex_string(e):
                logger.error('%s, Please check it in the script: %s' %(e,module.__name__))
            elif 'Function is not exist.' in get_safe_ex_string(e):
                logger.error(
                    'Function is not exist, Please check \'%s\' in the script: %s' % (self.func_name, module.__name__,))
            else:
                logger.error("%s %s:%s for %s:%d" % (e, module.__name__, self.func_name, host, port ))
            self.change_error_count(1)
        except KeyError as e:
            logger.error("Missing parameters: %s, please load parameters by -p. For example. -p %s=value" % (
            e, str(e).replace('\'', '')))
        except Exception as e:
            self.errmsg = traceback.format_exc()
            self.is_continue = False
            logger.error(self.errmsg)


    def get_data(self):
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

    def filter(self, module, service = None):
        '''
        filter unnecessary module by service
        :param module:
        :param service:
        :return:
        '''
        poc = module.POC()
        if service != None:
            if poc.service_type[0] != service:
                # Not web service
                if poc.service_type[0] in SERVICE_NOT_WEB_LIST:
                    return True
                    # else:
                    #
                    #     脚本web  服务非web
        return False

    def put_queue(self):
        id = 0
        for host in self.targets.keys():
            id += 1
            for module in self.modules:
                if len(self.targets[host].keys()) == 1:
                    '''
                    Set the port for no port scan model, e.g.
                        -iS http://www.baidu.com/aaaa
                        -iS www.baidu.com:80
                    '''
                    if conf['noportscan']:
                        for port, values in self.targets[host].items():
                            for service, url in values:

                                if self.filter(module,service):
                                    continue

                                self.total += 1
                                self.queue.put([id, module, (host, port, service, url)])

                else:

                    '''
                    Don't set the port, e.g.
                        -iN 192.168.111.1/24
                        -iS www.baidu.com

                    Add  the modules' all ports
                    '''
                    poc = module.POC()
                    service, ports = poc.service_type
                    if isinstance(ports, list):
                        for port in ports:
                            if port in self.targets[host].keys():
                                continue
                            _ = (service, None)

                            if not conf['noportscan']:
                                self._put_target(host, port, _)
                            else:
                                self.total += 1
                                self.queue.put([id, module, (host, port, service, None)])


                    elif isinstance(ports, int):
                        _ = (service, None)
                        if not conf['noportscan']:
                            self._put_target(host, ports, _)
                        else:
                            self.total += 1
                            self.queue.put([id, module, (host, ports, service, None)])

            # Scan port and match service for port scan model
            if not conf['noportscan'] :
                module = self._load_module('script.info.port_scan')
                if module ==None:
                    logger.error("Invalid POC script, Please check the script: script.info.port_scan")
                self.total += len(self.targets[host].keys())
                for port, values in self.targets[host].items():
                    self.total += len(values) - 1
                    for service, url in values:
                        self.queue.put([id, module, (host, port, service, url)])
                        if self.queue.qsize() >= self.queue_pool_cache:
                            yield self.queue
        yield self.queue


    def put_queue_by_res(self,id, ex_module, host, port, service, url):
        for module in self.modules:
            # Bypass itself
            if module.__name__ == ex_module.__name__:
                continue

            if self.filter(module, service):
                continue

            self.total += 1
            self.queue.put([id, module, (host, port, service, url)])
            if self.queue.qsize() >= self.queue_pool_cache:
                yield self.queue
        yield self.queue

    def _load_module(self,module_name):
        module_spec = importlib.util.find_spec(module_name)

        if module_spec:
            try:
                module = importlib.import_module(module_name)
                if 'POC' not in dir(module):
                    logger.error('Invalid POC script, Please check the script: %s' % module.__name__)
                else:
                    return module
            except Exception as e:
                logger.error('Invalid POC script, Please check the script: %s' % module_name)
                logger.error(get_safe_ex_string(e))
        else:
            logger.error('Can\'t load modual: %s.' % conf.module_path)

        return None

    def load_modules(self):
        modules_name = conf['modules_name']
        func_name = conf['func_name']

        if len(modules_name) < 0:
            msg = 'Can\'t find any modules. Please check you input.'
            sys.exit(logger.error(msg))

        elif len(modules_name) == 1:
            logger.sysinfo('Loading modual: %s' % (modules_name[0]))
            module = self._load_module(modules_name[0])
            if module == None:
                logger.error("Invalid POC script, Please check the script: %s" %modules_name[0])
                sys.exit()

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
                msg += "\r\n| Default Port: " + str(poc.service_type if 'service_type' in poc.__dict__ else 'unknown')
                msg += "\r\n ------------------------------- "
                logger.sysinfo(msg)
                sys.exit()

            self.modules.append(module)

        else:
            modules = []
            logger.sysinfo('Loading moduals...')
            for module_name in conf['modules_name']:
                module = self._load_module(module_name)
                if module == None:
                    logger.error("Invalid POC script, Please check the script: %s" % module_name)
                    continue
                modules.append(module)
                if len(self.modules) > 1 and func_name.lower() in  ['show','help']:
                    sys.exit(logger.error('Can\'t show so many modules.'))

            # sort
            self.modules = sorted(modules, key=lambda modules: modules.POC().priority)


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

    def put_target(self, target, service=None):
        '''
        :param target: host:port or url
        :param service:
        :return:
        '''
        if target.startswith('http://') or target.startswith('https://'):
            protocol, s1 = urllib.parse.splittype(target)
            host, s2 = urllib.parse.splithost(s1)
            host, port = urllib.parse.splitport(host)
            port = int(port) if port != None and port != 0 else 443 if protocol == 'https' else 80
            _ = (SERVICE_PORT_MAP.WEB[0], target)
        elif ":" in target:
            _v = target.split(':')
            host, port = _v[0], int(_v[1])
            _ = (service, None)
        else:
            host = target
            port = None
            _ = (None,None)
        self._put_target(host, port , _)

    def _put_target(self, host, port, _=(None,None)):
        if host not in self.targets.keys():
            self.targets[host] = {}
        if port:
            if port in self.targets[host].keys():
                self.targets[host][port].append(_)
            else:
                self.targets[host][port] = [_]
        else:
            self.targets[host] = {}
        if len(self.targets) > self.target_pool_total:
            msg = 'Too many targets! Please control the target\'s numbers under the %d.' % self.target_pool_total
            sys.exit(logger.error(msg))

    def _load_target(self,target, service=None):

        # http://localhost
        if target.startswith('http://') or target.startswith('https://'):
            self.put_target(target,service)
        else:

            # 192.168.111.1/24
            if '/' in target and check_ippool(target):
                for each in build(target):
                    self.put_target(each, service)

            # 192.168.111.1-192.168.111.3
            elif '-' in target and check_ippool(target):
                _v = target.split('-')
                for each in build(_v[0], _v[1]):
                    self.put_target(each, service)

            # 192.168.111.1
            else:
                target = target[:-1] if target[-1] == '/' else target
                if ":" in target:
                    self.put_target(target, service)
                else:
                    self.put_target(target, service)


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
                        self._load_target(':'.join([host_id,str(port_id)]), port_service)
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
                    self._load_target(':'.join([_row[3], str(_row[4])]))
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
                    self._load_target(_url, _server)

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

    def print_progress(self):
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

    def set_thread_daemon(self,thread):
        thread.setDaemon(True)