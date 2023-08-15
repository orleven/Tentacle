#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from lib.core.g import async_engine_sqlite_task
from lib.core.g import async_engine_sqlite_task_data
from lib.util.util import get_time
from lib.util.util import get_time_str

TaskBase = declarative_base(async_engine_sqlite_task)

TaskDataBase = declarative_base(async_engine_sqlite_task_data)

class Task(TaskBase):
    """任务"""
    __tablename__ = "task"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    task_name = Column(String(32), unique=True)
    engine = Column(String(255))
    status = Column(String(32))
    value = Column(Text())
    update_time = Column(DateTime(), default=get_time())

    def to_json(self):
        json_data = {
            "id": self.id,
            "task_name": self.task_name,
            "status": self.status,
            "engine": self.engine,
            "value": self.value,
            "update_time": get_time_str(self.update_time) if self.update_time else None,
        }
        return json_data

class Vul(TaskDataBase):
    """漏洞"""
    __tablename__ = "vul"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    task_name = Column(String(10))
    scheme = Column(String(10))
    host = Column(String(255))
    port = Column(Integer())
    url = Column(Text())
    # vul_name = Column(String(255))
    # level = Column(String(255))
    # vul_type = Column(String(255))
    # description = Column(Text())
    # scopen = Column(Text())
    # impact = Column(Text())
    # suggestions = Column(Text())
    detail = Column(Text())
    mark = Column(Text())
    update_time = Column(DateTime(), default=get_time())
    script_path = Column(String(255))
    script_name = Column(String(255))

    def to_json(self):
        json_data = {
            "id": self.id,
            "task_name": self.task_name,
            "scheme": self.scheme,
            "host": self.host,
            "port": self.port,
            "url": self.url,
            "detail": self.detail,
            # "vul_type": self.vul_type,
            # "vul_name": self.vul_name,
            # "level": self.level,
            # "description": self.description,
            # "suggestions": self.suggestions,
            # "impact": self.impact,
            # "scopen": self.scopen,
            "update_time": get_time_str(self.update_time) if self.update_time else None,
            "script_path": self.script_path,
            "script_name": self.script_name,
            "mark": self.mark,
        }
        return json_data
