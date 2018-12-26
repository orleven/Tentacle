#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import sqlite3
from lib.core.data import logger
from lib.core.common import get_safe_ex_string
from lib.core.common import serialize_object

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
        self.execute("CREATE TABLE IF NOT EXISTS task("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "taskid TEXT, status INTEGER, task_value TEXT, update_time TEXT"
        ")")

