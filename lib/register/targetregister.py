#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import asyncio
import re
from copy import copy
from xml.etree import ElementTree as ET
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from lib.api.fofa import get_fofa_api
from lib.api.google import get_google_api
from lib.api.searchengine import get_search_engine_api
from lib.api.shodan import get_shodan_api
from lib.api.zoomeye import get_zoomeye_api
from lib.core.env import *
from urllib.parse import urlparse
from lib.core.g import log
from lib.core.g import conf
from lib.core.data import query_all_vul
from lib.core.enums import ServicePortMap
from lib.core.enums import TargetStatus
from lib.core.sqlite import SQLite
from lib.register import BaseRegister
from lib.util.iputil import build
from lib.util.iputil import check_ippool
from lib.util.util import output_excal


class TargetRegister(BaseRegister):
    """
    TargetRegister
    """

    def __init__(self):
        self.target_port_list = []

    async def get_history_data(self, task):
        sqlite_task_data = SQLite(
            dbname=task,
        )
        async_sqlalchemy_sqlite_task_data_database_url = sqlite_task_data.get_async_sqlalchemy_database_url()
        async_engine_sqlite_task_data = create_async_engine(async_sqlalchemy_sqlite_task_data_database_url)
        async_session_sqlite_task_data = sessionmaker(async_engine_sqlite_task_data, class_=AsyncSession)
        data_list = await query_all_vul(async_session_sqlite_task_data)
        return data_list

    async def register_target(self):
        if conf.scan.simple:
            log.info(f"Loading target {conf.scan.simple}... ")
            async for target in self.register_host(conf.scan.simple):
                yield target

        if conf.scan.file:
            if os.path.isfile(conf.scan.file):
                log.info(f"Loading target {conf.scan.file}... ")
                with open(conf.scan.file, 'r') as f:
                    for line in f.readlines():
                        line = line.replace("\r", "").replace("\n", "").strip().rstrip()
                        if line and line != '':
                            async for target in self.register_host(line):
                                yield target
            else:
                log.error(f"Target file not exist: {conf.scan.file}...")
                sys.exit(0)

        if conf.scan.nmap_xml:
            if os.path.isfile(conf.scan.nmap_xml):
                log.info(f"Loading target {conf.scan.nmap_xml}... ")
                tree = ET.parse(conf.scan.nmap_xml)
                root = tree.getroot()
                for host in root.findall('host'):
                    host_id = host.find('address').get('addr')
                    for port in host.iter('port'):
                        port_id = port.attrib.get('portid')
                        # port_protocol = port.attrib.get('protocol')
                        port_state = port.find('state').attrib.get('state')
                        try:
                            port_service = port.find('service').attrib.get('name')
                        except:
                            port_service = None
                        if port_state.lower() not in ['closed', 'filtered']:
                            address = ':'.join([host_id, str(port_id)])
                            async for target in self.register_host(address, port_service):
                                yield target
            else:
                log.error(f"Target file not exist: {conf.scan.nmap_xml}...")
                sys.exit(0)

        if conf.scan.task:
            log.info(f"Loading target {conf.scan.task}... ")
            address_list = []
            data_list = await self.get_history_data(conf.scan.task)
            if data_list:
                for item in data_list:
                    url = item.get('url', None)
                    if url:
                        address = url
                    else:
                        host = item.get('host', None)
                        if host:
                            port = item.get('port', None)
                            if port:
                                address = host + ':' + port
                            else:
                                address = host
                        else:
                            continue
                    address_list.append(address)
            address_list = list(set(address_list))
            for address in address_list:
                async for target in self.register_host(address):
                    yield target

        if conf.scan.search_engine:
            log.info(f"Loading target {conf.scan.search_engine}... ")
            async for item in get_search_engine_api(conf.scan.search_engine):
                async for target in self.register_host(item):
                    yield target

        if conf.scan.zoomeye:
            log.info(f"Loading target {conf.scan.zoomeye}... ")
            for z_type in ['host', 'web']:
                async for item in get_zoomeye_api(conf.scan.zoomeye, z_type=z_type):
                    async for target in self.register_host(item):
                        yield target

        if conf.scan.shodan:
            log.info(f"Loading target {conf.scan.shodan}... ")
            async for item in get_shodan_api(conf.scan.shodan):
                async for target in self.register_host(item):
                    yield target

        if conf.scan.fofa:
            log.info(f"Loading target {conf.scan.fofa}... ")
            async for item in get_fofa_api(conf.scan.fofa):
                async for target in self.register_host(item):
                    yield target

        if conf.scan.google:
            log.info(f"Loading target {conf.scan.google}... ")
            async for item in get_google_api(conf.scan.google):
                async for target in self.register_host(item):
                    yield target

    def register_port(self):

        limit_port = []

        for port_scope in conf.scan.limit_port_scan.lower().split(','):
            port_scope = port_scope.strip().rstrip()
            if '-' in port_scope:
                try:
                    pattern = re.compile(r'(\d+)-(\d+)')
                    match = pattern.match(port_scope)
                    if match:
                        start_port = int(match.group(1))
                        end_port = int(match.group(2))
                        if start_port > 0 and start_port < 65536 and end_port > 0 and end_port < 65536:
                            limit_port += [x for x in range(start_port, end_port + 1)]
                        else:
                            log.error("Illegal input: %s" % port_scope)
                            sys.exit(0)
                    else:
                        log.error("Illegal input: %s" % port_scope)
                        sys.exit(0)
                except Exception as err:
                    log.error("Illegal input: %s" % port_scope)
                    sys.exit(0)
            elif 'top' in port_scope or 'all' == port_scope or '*' == port_scope:
                if 'top10' == port_scope:
                    limit_port += [x for x in ServicePortMap.TOP10[1]]
                elif 'top50' == port_scope:
                    limit_port += [x for x in ServicePortMap.TOP50[1]]
                elif 'top100' == port_scope:
                    limit_port += [x for x in ServicePortMap.TOP100[1]]
                elif 'top150' == port_scope:
                    limit_port += [x for x in ServicePortMap.TOP150[1]]
                elif 'top1000' == port_scope:
                    limit_port += [x for x in ServicePortMap.TOP100[1]]
                elif 'all' == port_scope or '*' == port_scope:
                    limit_port += [x for x in range(1, 65536)]
                else:
                    log.error("Illegal input: %s" % port_scope)
                    sys.exit(0)
            else:
                try:
                    start_port = int(port_scope)
                    if start_port > 0 and start_port < 65536:
                        limit_port.append(start_port)
                    else:
                        log.error("Illegal input: %s" % port_scope)
                        sys.exit(0)
                except:
                    log.error("Illegal input: %s" % port_scope)
                    sys.exit(0)
        self.target_port_list = list(set(limit_port))

    async def register_host(self, target, service=None):
        # http://localhost
        if re.compile(r'^[a-zA-Z]{2,8}://').match(target):
            if '/' not in target.replace("://", ""):
                target += '/'
            target_arr = urlparse(target)
            protocol = target_arr.scheme
            host = target_arr.hostname
            port = target_arr.port
            port = int(port) if port and port != 0 else 443 if protocol == 'https' else 80
            yield self.standard_target(url=target, protocol=protocol, port=port, host=host, service=service)
        else:
            # 192.168.111.1/24
            if '/' in target and check_ippool(target):
                for each in build(target):
                    yield self.standard_target(host=each, service=service)

            # 192.168.111.1-192.168.111.3
            elif '-' in target and check_ippool(target):
                v = target.split('-')
                start_ip = v[0].strip().rstrip()
                end_ip = v[1].strip().rstrip()
                for each in build(start_ip, end_ip):
                    yield self.standard_target(host=each, service=service)

            # 192.168.111.1:80
            elif ':' in target:
                v = target.split(':')
                host = v[0].strip().rstrip()
                port = int(v[1].strip().rstrip())
                yield self.standard_target(host=host, port=port, service=service)

            # 192.168.111.1
            else:
                target = target[:-1] if target[-1] == '/' else target
                yield self.standard_target(host=target, service=service)


    def standard_target(self, host=None, port=None, service=None, url=None, base_url=None, protocol=None,
            banner=None, fingerprint=None, status=TargetStatus.INIT):
        target = {'host': host, 'port': port, 'service': service, 'protocol': protocol, 'banner': banner,
         'fingerprint': fingerprint, 'url': url, 'base_url': base_url, 'status': status, 'port_connect': None}
        return target

    async def load_target_ping(self):
        async for target in self.register_target():
            yield target

    async def load_target_by_target(self, target):
        if (conf.scan.skip_port_scan and conf.scan.limit_port_scan) or \
                (not conf.scan.skip_port_scan and conf.scan.limit_port_scan):
            if conf.scan.limit_port_scan:
                if len(self.target_port_list) == 0:
                    self.register_port()
                for port in self.target_port_list:
                    temp_target = copy(target)
                    temp_target["port"] = port
                    yield temp_target
            else:
                yield target
        else:
            yield target

    async def load_target_no_ping(self):
        async for target in self.register_target():
            if target.get("url", None):
                yield target
            else:
                if target.get("port", None):
                    yield target
                else:
                    async for temp_target in self.load_target_by_target(target):
                        yield temp_target


    async def print_task(self, task_show):
        data_list = await self.get_history_data(task_show)
        if data_list:
            for result in data_list:
                address = result["url"] if result.get("url", None) else f'{result["host"]}:{result["port"]}'
                msg = f'[{result["script_path"]}] [{address}]: {result["detail"]}'
                log.success(msg)

        if conf.basic.out:
            log.info(f'[{task_show}] Task export to {conf.basic.out}')
            output_excal(data_list, conf.basic.out)

    def start_print(self, task_show):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.print_task(task_show))
        except:
            pass



