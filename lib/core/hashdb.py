#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import os
import time
import queue
import sqlite3
import threading
from lib.core.data import logger
from lib.core.common import serialize_object
from lib.core.common import unserialize_object
from lib.core.data import conf, logger,paths
from lib.core.common import get_safe_ex_string
from lib.core.settings import HASHDB_FLUSH_RETRIES
from lib.core.settings import HASHDB_FLUSH_THRESHOLD
from lib.core.settings import HASHDB_RETRIEVE_RETRIES
from lib.core.settings import HASHDB_END_TRANSACTION_RETRIES
from lib.core.exception import TentacleConnectionException

'''
{'flag': True, 'data': [], 'res': [{'info': '网易', 'key': 'login,登陆', 'status': '200', 'encoding': 'GBK'}], 'tid': 0, 'url': 'https://www.163.com', 'target_host': 'www.163.com', 'target_port': 443}
'''
class HashDB(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.connection = None
        self._write_cache = queue.Queue()
        self.cursor = None
        self._cache_lock = threading.Lock()

    def connect(self, who="hashdb"):
        self.connection = sqlite3.connect(self.filepath, timeout=3, isolation_level=None, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()

    def commit(self):
        self.connection.commit()

    def execute(self, statement, arguments=None):
        while True:
            try:
                if arguments:
                    self.cursor.execute(statement, arguments)
                else:
                    self.cursor.execute(statement)
            except sqlite3.OperationalError as ex:
                if not "locked" in get_safe_ex_string(ex):
                    raise
            else:
                break

        if statement.lstrip().upper().startswith("SELECT"):
            return self.cursor.fetchall()

    def init(self):
        self.execute(
            "CREATE TABLE IF NOT EXISTS storage ("
            "id INTEGER PRIMARY KEY, "
            "tid INTEGER, "
            "flag INTEGER, "
            "target_host TEXT, target_port TEXT,url TEXT, module_name TEXT,"
            "data TEXT, res TEXT, other TEXT"
            ")")

    def insert(self,data):
        self._write_cache.put(data)

    def select_all(self):
        return self.execute("SELECT * FROM storage")


    def flush(self):
        while True:
            self._cache_lock.acquire()
            if self._write_cache.qsize() >0 :
                data = self._write_cache.get()
                self._cache_lock.release()
            else:
                self._cache_lock.release()
                break
            retries = 0
            while True:
                try:

                    self._cache_lock.acquire()
                    self.execute(
                        "INSERT INTO storage (tid,flag,target_host,target_port,url,module_name,data,res,other) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (data['id'], data['flag'], data['target_host'], data['target_port'], data['url'], data['module_name'],
                         serialize_object(data['data']), serialize_object(data['res']),
                         serialize_object(data['other'])))
                except sqlite3.DatabaseError as ex:
                    if not os.path.exists(self.filepath):
                        debugMsg = "session file '%s' does not exist" % self.filepath
                        logger.debug(debugMsg)
                        break

                    if retries == 0:
                        warnMsg = "there has been a problem while writing to "
                        warnMsg += "the session file ('%s')" % get_safe_ex_string(ex)
                        logger.warn(warnMsg)

                    if retries >= HASHDB_FLUSH_RETRIES:
                        return
                    else:
                        retries += 1
                        time.sleep(1)

                    self._cache_lock.release()
                else:

                    self._cache_lock.release()
                    break

