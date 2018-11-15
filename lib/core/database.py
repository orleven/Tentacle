#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import sqlite3
from lib.core.data import logger
from lib.core.common import get_safe_ex_string
from lib.core.common import serialize_object

# API objects
class Database(object):
    filepath = None

    def __init__(self, database=None):
        self.database = self.filepath if database is None else database
        self.connection = None
        self.cursor = None

    def connect(self, who="storage"):
        self.connection = sqlite3.connect(self.database, timeout=3, isolation_level=None, check_same_thread=False)
        self.cursor = self.connection.cursor()
        # logger.debug("Connected to IPC database %s" % who)

    def disconnect(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()

    def commit(self):
        self.connection.commit()

    def insert_task(self, taskid,task_value,status):

        self.execute("INSERT INTO task (taskid,task_value,status) VALUES (?, ?, ?)",(taskid,serialize_object(task_value),status,))

    def update_task_status(self, taskid, status ):
        self.execute("UPDATE task set status = ? WHERE taskid = ?",(status,taskid))

    def detele_task(self, taskid):
        self.execute("DELETE from task WHERE taskid = ?",(taskid))

    def select_all(self):
        return self.execute("SELECT * FROM task")

    def select(self,taskid):
        return self.execute("SELECT * FROM task WHERE taskid = ?" ,(taskid,))

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
        # self.execute("CREATE TABLE logs("
        #           "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        #           "taskid INTEGER, time TEXT, "
        #           "level TEXT, message TEXT"
        #           ")")

        self.execute("CREATE TABLE IF NOT EXISTS task("
                  "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                  "taskid TEXT, status INTEGER,  task_value TEXT"
                  ")")

        # self.execute("CREATE TABLE errors("
        #             "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        #             "taskid INTEGER, error TEXT"
        #             ")")