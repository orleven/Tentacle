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
from lib.core.enums import ENGINE_MODE_STATUS
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
        # self._write_cache = {}
        self.connection = None
        self._write_cache = queue.Queue()
        self.cursor = None
        self._cache_lock = threading.Lock()

    def connect(self, who="hashdb"):
        self.connection = sqlite3.connect(self.filepath, timeout=3, isolation_level=None, check_same_thread=False)
        self.cursor = self.connection.cursor()
        # logger.debug("Connected to hashdb database: %s" % who)

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






    # def _get_cursor(self):
    #     threadData = getCurrentThreadData()
    #
    #     if threadData.hashDBCursor is None:
    #         try:
    #             connection = sqlite3.connect(self.filepath, timeout=3, isolation_level=None)
    #             threadData.hashDBCursor = connection.cursor()
    #             threadData.hashDBCursor.execute(
    #                 "CREATE TABLE IF NOT EXISTS storage ("
    #                 "id INTEGER PRIMARY KEY, "
    #                 "flag NUMERIC "
    #                 "target_host TEXT, target_port TEXT,url TEXT, "
    #                 "data TEXT, res TEXT, other TEXT"
    #                 ")")
    #             connection.commit()
    #         except Exception as  ex:
    #             errMsg = "error occurred while opening a session "
    #             errMsg += "file '%s' ('%s')" % (self.filepath, getSafeExString(ex))
    #             raise TentacleConnectionException(errMsg)
    #
    #     return threadData.hashDBCursor

    # def _set_cursor(self, cursor):
    #     threadData = getCurrentThreadData()
    #     threadData.hashDBCursor = cursor

    # cursor = property(_get_cursor, _set_cursor)

    # def close(self):
    #     threadData = getCurrentThreadData()
    #     try:
    #         if threadData.hashDBCursor:
    #             threadData.hashDBCursor.close()
    #             threadData.hashDBCursor.connection.close()
    #             threadData.hashDBCursor = None
    #     except:
    #         pass

    # @staticmethod
    # def hashKey(key):
    #     key = key.encode(UNICODE_ENCODING) if isinstance(key, unicode) else repr(key)
    #     retVal = int(hashlib.md5(key).hexdigest(), 16) & 0x7fffffffffffffff  # Reference: http://stackoverflow.com/a/4448400
    #     return retVal



    # def retrieve(self, key, unserialize=False):
    #     retVal = None
    #
    #     if key and (self._write_cache or os.path.isfile(self.filepath)):
    #         hash_ = HashDB.hashKey(key)
    #         retVal = self._write_cache[hash_]
    #         if retVal !=None:
    #             for _ in range(HASHDB_RETRIEVE_RETRIES):
    #                 try:
    #                     for row in self.cursor.execute("SELECT value FROM storage WHERE id=?", (hash_,)):
    #                         retVal = row[0]
    #                 except sqlite3.OperationalError as ex:
    #                     if any(_ in getSafeExString(ex) for _ in ("locked", "no such table")):
    #                         warnMsg = "problem occurred while accessing session file '%s' ('%s')" % (self.filepath, getSafeExString(ex))
    #                         singleTimeWarnMessage(warnMsg)
    #                     elif "Could not decode" in getSafeExString(ex):
    #                         break
    #                     else:
    #                         raise
    #                 except sqlite3.DatabaseError as ex:
    #                     errMsg = "error occurred while accessing session file '%s' ('%s'). " % (self.filepath, getSafeExString(ex))
    #                     errMsg += "If the problem persists please rerun with `--flush-session`"
    #                     raise (TentacleConnectionException , errMsg)
    #                 else:
    #                     break
    #
    #                 time.sleep(1)
    #
    #     if retVal and unserialize:
    #         try:
    #             retVal = unserializeObject(retVal)
    #         except:
    #             retVal = None
    #             warnMsg = "error occurred while unserializing value for session key '%s'. " % key
    #             warnMsg += "If the problem persists please rerun with `--flush-session`"
    #             logger.warn(warnMsg)
    #
    #     return retVal


    # def write(self, data):
    #     self._cache_lock.acquire()
    #     self._write_cache.append(data)
    #     self._cache_lock.release()
    #
    #     if getCurrentThreadName() in ('0', 'MainThread'):
    #         self.flush()

    # def write(self, key, value, serialize=False):
    #     if key:
    #         hash_ = HashDB.hashKey(key)
    #         self._cache_lock.acquire()
    #         self._write_cache[hash_] = getUnicode(value) if not serialize else serializeObject(value)
    #         self._cache_lock.release()
    #
    #     if getCurrentThreadName() in ('0', 'MainThread'):
    #         self.flush()

    # def flush(self, forced=False):
    #     if not self._write_cache:
    #         return
    #
    #     if not forced and len(self._write_cache) < HASHDB_FLUSH_THRESHOLD:
    #         return
    #
    #     self._cache_lock.acquire()
    #     datas = self._write_cache
    #     self._write_cache = []
    #     self._cache_lock.release()
    #
    #     try:
    #         self.beginTransaction()
    #         "CREATE TABLE IF NOT EXISTS storage ("
    #         "id INTEGER PRIMARY KEY, "
    #         "target_host TEXT, target_port TEXT,url TEXT, "
    #         "data TEXT, res TEXT, "
    #         "other TEXT, flag NUMERIC"
    #         ")"
    #         for data in datas:
    #             retries = 0
    #             while True:
    #                 try:
    #                     self.cursor.execute(
    #                         "INSERT INTO storage (id,flag,target_host,target_port,url,data,res,other) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    #                         (data['id'], data['flag'], data['target_host'], data['target_port'], data['url'],
    #                          serializeObject(data['data']), serializeObject(data['res']),
    #                          serializeObject(data['other'])))
    #
    #                 except sqlite3.DatabaseError as ex:
    #                     if not os.path.exists(self.filepath):
    #                         debugMsg = "session file '%s' does not exist" % self.filepath
    #                         logger.debug(debugMsg)
    #                         break
    #
    #                     if retries == 0:
    #                         warnMsg = "there has been a problem while writing to "
    #                         warnMsg += "the session file ('%s')" % getSafeExString(ex)
    #                         logger.warn(warnMsg)
    #
    #                     if retries >= HASHDB_FLUSH_RETRIES:
    #                         return
    #                     else:
    #                         retries += 1
    #                         time.sleep(1)
    #                 else:
    #                     break
            # for hash_, value in _.items():
            #     retries = 0
            #     while True:
            #         try:
            #
            #             try:
            #                 self.cursor.execute("INSERT INTO storage VALUES (?, ?)", (hash_, value,))
            #             except sqlite3.IntegrityError:
            #                 self.cursor.execute("UPDATE storage SET value=? WHERE id=?", (value, hash_,))
            #         except sqlite3.DatabaseError as ex:
            #             if not os.path.exists(self.filepath):
            #                 debugMsg = "session file '%s' does not exist" % self.filepath
            #                 logger.debug(debugMsg)
            #                 break
            #
            #             if retries == 0:
            #                 warnMsg = "there has been a problem while writing to "
            #                 warnMsg += "the session file ('%s')" % getSafeExString(ex)
            #                 logger.warn(warnMsg)
            #
            #             if retries >= HASHDB_FLUSH_RETRIES:
            #                 return
            #             else:
            #                 retries += 1
            #                 time.sleep(1)
            #         else:
            #             break
        # finally:
        #     self.endTransaction()

    # def beginTransaction(self):
    #     threadData = getCurrentThreadData()
    #     if not threadData.inTransaction:
    #         try:
    #             self.cursor.execute("BEGIN TRANSACTION")
    #         except:
    #             # Reference: http://stackoverflow.com/a/25245731
    #             self.cursor.close()
    #             threadData.hashDBCursor = None
    #             self.cursor.execute("BEGIN TRANSACTION")
    #         finally:
    #             threadData.inTransaction = True
    #
    # def endTransaction(self):
    #     threadData = getCurrentThreadData()
    #     if threadData.inTransaction:
    #         retries = 0
    #         while retries < HASHDB_END_TRANSACTION_RETRIES:
    #             try:
    #                 self.cursor.execute("END TRANSACTION")
    #                 threadData.inTransaction = False
    #             except sqlite3.OperationalError:
    #                 pass
    #             else:
    #                 return
    #
    #             retries += 1
    #             time.sleep(1)
    #
    #         try:
    #             self.cursor.execute("ROLLBACK TRANSACTION")
    #         except sqlite3.OperationalError:
    #             self.cursor.close()
    #             self.cursor = None
    #         finally:
    #             threadData.inTransaction = False
