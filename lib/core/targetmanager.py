#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import os
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from lib.core.enums import SERVICE_PORT_MAP
from lib.core.enums import API_TYPE
from lib.utils.iputil import build
from lib.utils.iputil import check_ippool
from lib.core.data import logger
from lib.core.data import paths
from lib.api.api import search_api
from lib.core.database import TaskDataDB

class TargetManager:

    def __init__(self, input_target):
        self.target_simple = None
        self.target_file = None
        self.target_nmap_xml = None
        self.target_network = None
        self.target_task = None
        self.target_search_engine = None
        self.target_zoomeye = None
        self.target_shodan = None
        self.target_fofa = None
        # self.target_fofa_today_poc = None
        self.target_google = None
        self.target_pool_total = 65535 * 10

        self._target_register(input_target)
        # self.targets = {}

    def _target_register(self, input_target):

        if input_target.target_simple:
            self.target_simple = input_target.target_simple
            logger.debug("Add target: %s" % self.target_simple)

        if input_target.target_file:
            if os.path.isfile(input_target.target_file):
                self.target_file = input_target.target_file
            else:
                msg = 'Target file not exist: %s' % input_target.target_file
                sys.exit(logger.error(msg))
            logger.debug("Add target: %s" % self.target_file)

        if input_target.target_nmap_xml:
            if os.path.isfile(input_target.target_nmap_xml):
                self.target_nmap_xml = input_target.target_nmap_xml
            else:
                msg = 'Target file not exist: %s' % input_target.target_nmap_xml
                sys.exit(logger.error(msg))
            logger.debug("Add target: %s" % self.target_nmap_xml)

        if input_target.target_network:
            self.target_network = input_target.target_network
            logger.debug("Add target: %s" % self.target_network)

        if input_target.target_task:
            self.target_task = input_target.target_task
            logger.debug("Add target: %s" % self.target_task)

        if input_target.target_search_engine:
            self.target_search_engine = input_target.target_search_engine
            logger.debug("Add target: %s" % self.target_search_engine)

        if input_target.target_zoomeye:
            self.target_zoomeye = input_target.target_zoomeye
            logger.debug("Add target: %s" % self.target_zoomeye)

        if input_target.target_shodan:
            self.target_shodan = input_target.target_shodan
            logger.debug("Add target: %s" % self.target_shodan)

        if input_target.target_fofa:
            self.target_fofa = input_target.target_fofa
            logger.debug("Add target: %s" % self.target_fofa)

        # if input_target.target_fofa_today_poc:
        #     self.target_fofa_today_poc = input_target.target_fofa_today_poc
        #     logger.debug("Add target: %s" % self.target_fofa_today_poc)

        if input_target.target_google:
            self.target_google = input_target.target_google
            logger.debug("Add target: %s" % self.target_google)

    async def load(self):
        no = 0
        if self.target_simple != None:
            logger.sysinfo("Loading target: %s" % (self.target_simple))
            for target in self._load_target(no+1,self.target_simple):
                yield target


        if self.target_file != None:
            with open(self.target_file, 'r') as f:
                logger.sysinfo("Loading target: %s" % (self.target_file))
                for _line in f.readlines():
                    no += 1
                    line = _line.replace("\r","").replace("\n","").strip()
                    if line and line != '':
                        for li in  self._load_target(no, line):
                            yield li


        if self.target_nmap_xml != None:
            logger.sysinfo("Loading target: %s" % (self.target_nmap_xml))
            tree = ET.parse(self.target_nmap_xml)
            root = tree.getroot()
            for host in root.findall('host'):
                host_id = host.find('address').get('addr')
                # infoLit = []
                for port in host.iter('port'):
                    no += 1
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
                        yield self._load_target(no, ':'.join([host_id,str(port_id)]), port_service)
                # resDic = {"host": host_id, "info": infoLit}
                # resLit.append(resDic)


        if self.target_network != None:
            logger.sysinfo("Loading target: %s" % (self.target_network))
            for target in self._load_target(no+1, self.target_network,):
                yield target


        if self.target_task != None:
            logger.sysinfo("Loading target: %s" % (self.target_task))
            hashdb = TaskDataDB(os.path.join(paths.DATA_PATH,self.target_task))
            hashdb.connect()
            for _row in hashdb.select_all():
                no += 1
                if _row[5] != None and _row[5] != '':
                    for target in self._load_target(no, _row[5]):
                        yield target
                else:
                    for target in self._load_target(no, ':'.join([_row[3], str(_row[4])]) ):
                        yield target


        if self.target_search_engine != None:
            logger.sysinfo("Loading target by baidu/bing/360so: %s" % (self.target_search_engine))
            urls = await search_api(self.target_search_engine, type=API_TYPE.OTHER_SEARCH_ENGINE)
            for _url in urls:
                if _url:
                    no += 1
                    for target in self._load_target(no, _url):
                        yield target

        if self.target_zoomeye != None:
            logger.sysinfo("Loading target by zoomeye: %s" % (self.target_zoomeye))
            urls = await search_api(self.target_zoomeye, type=API_TYPE.ZOOMEYE)
            for _url in urls:
                if _url:
                    no += 1
                    for target in self._load_target(no, _url):
                        yield target

        if self.target_shodan != None:
            logger.sysinfo("Loading target by shadon: %s" % (self.target_shodan))
            urls = await search_api(self.target_shodan, type=API_TYPE.SHODAN)
            for _url in urls:
                if _url:
                    no += 1
                    for target in self._load_target(no, _url):
                        yield target

        if self.target_fofa != None:
            logger.sysinfo("Loading target by fofa: %s" % (self.target_fofa))
            urls = await search_api(self.target_fofa, type=API_TYPE.FOFA)
            for _url in urls:
                if _url:
                    no += 1
                    for target in self._load_target(no, _url):
                        yield target

        # if self.target_fofa_today_poc != None:
        #     logger.sysinfo("Loading target by fofa today poc: %s" % (self.target_fofa_today_poc))
        #     obj = await search_api(self.target_fofa_today_poc, type=API_TYPE.FOFA_TODAY_POC)
        #     for _url,_server in obj:
        #         if _url:
        #             no += 1
        #             for target in self._load_target(no, _url, _server):
        #                 yield target

        if self.target_google != None:
            logger.sysinfo("Loading target by google: %s" % (self.target_google))
            urls = await search_api(self.target_google, type=API_TYPE.GOOGLE)
            for _url in urls:
                if _url:
                    no += 1
                    for target in self._load_target(no, _url):
                        yield target

    async def load_from_list(self, targets):
        for target in targets:
            yield target

    def _load_target(self,no, target, service=None):

        # http://localhost
        if target.startswith('http://') or target.startswith('https://'):
            return [self.deal_target(no,target,service)]
        else:

            # 192.168.111.1/24
            if '/' in target and check_ippool(target):
                return [self.deal_target(no, each, service) for each in build(target)]


            # 192.168.111.1-192.168.111.3
            elif '-' in target and check_ippool(target):
                _v = target.split('-')
                return [self.deal_target(no,each, service) for each in build(_v[0], _v[1])]

            # 192.168.111.1
            else:
                target = target[:-1] if target[-1] == '/' else target
                return [self.deal_target(no,target, service)]

    def deal_target(self, no, target, service=None):
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
            _ = {'id':no, 'host': host, 'port':port , 'service': SERVICE_PORT_MAP.WEB[0], 'protocol':'tcp','banner':None, 'fingerprint':None,  'url': target, 'status': 3}
        elif ":" in target:
            _v = target.split(':')
            host, port = _v[0], int(_v[1])
            _ = {'id':no, 'host': host, 'port': port, 'service': service, 'protocol': None, 'banner': None,
                 'fingerprint': None, 'url': None, 'status': 3}
        else:
            _ = {'id':no, 'host': target, 'port': None, 'service': service, 'protocol': None, 'banner': None,
                 'fingerprint': None,  'url': None, 'status': 3}
        return _
