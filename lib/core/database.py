#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import os
import time
import queue
import sqlite3
import threading
from lib.core.data import logger
from lib.core.common import serialize_object
from lib.core.common import get_safe_ex_string

class Database(object):
    filepath = None

    def __init__(self, database=None):
        self.database = self.filepath if database is None else database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.database, timeout=3, isolation_level=None, check_same_thread=False)
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


class TaskDB(Database):
    '''
    {'flag': True, 'data': [], 'res': [{'info': '163', 'key': 'login', 'status': '200', 'encoding': 'GBK'}], 'tid': 0, 'url': 'https://www.163.com', 'target_host': 'www.163.com', 'target_port': 443}
    '''

    def insert_task(self, taskid,task_value,status, update_time):
        logger.debug("Insert task: %s" % (taskid))
        self.execute("INSERT INTO task (taskid, task_value, status, update_time) VALUES (?, ?, ?, ?)",(taskid,serialize_object(task_value),status, update_time))

    def update_task_status(self, taskid, status, update_time):
        logger.debug("Update task status to %s: %s" % (status,taskid))
        self.execute("UPDATE task set status = ?, update_time = ? WHERE taskid = ?",(status, update_time,taskid))

    def detele_task(self, taskid):
        self.execute("DELETE from task WHERE taskid = ?",(taskid,))

    def select_all(self):
        return self.execute("SELECT * FROM task ORDER BY update_time ASC")

    def select_taskid(self,taskid):
        return self.execute("SELECT * FROM task WHERE taskid = ?  ORDER BY update_time ASC" ,(taskid,))

    def init(self):
        self.execute("CREATE TABLE IF NOT EXISTS task("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "taskid TEXT, status INTEGER, task_value TEXT, update_time TEXT"
        ")")

class TaskDataDB(Database):
    def __init__(self, database):
        self._write_cache = queue.Queue()
        self._cache_lock = threading.Lock()
        super(TaskDataDB, self).__init__(database)

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
                         serialize_object(data['req']), serialize_object(data['res']),
                         serialize_object(data['other'])))
                except sqlite3.DatabaseError as ex:
                    if not os.path.exists(self.database):
                        debugMsg = "session file '%s' does not exist" % self.database
                        logger.debug(debugMsg)
                        break

                    if retries == 0:
                        warnMsg = "there has been a problem while writing to "
                        warnMsg += "the session file ('%s')" % get_safe_ex_string(ex)
                        logger.warn(warnMsg)

                    if retries >= 3:
                        return
                    else:
                        retries += 1
                        time.sleep(1)

                    self._cache_lock.release()
                else:

                    self._cache_lock.release()
                    break

