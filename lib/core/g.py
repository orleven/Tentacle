#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from lib.core.env import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from lib.core.log import Logger
from lib.core.sqlite import SQLite
from lib.core.config import config_parser
from lib.util.util import random_md5

# 配置存储
conf = config_parser()

# 日志
log = Logger(name=MAIN_NAME, use_console=True)

task_name = random_md5()[8:-8]

sqlite_task = SQLite(
    dbname=INDEX_DATABASE,
)

sqlite_task_data = SQLite(
    dbname=task_name,
)

async_sqlalchemy_sqlite_task_database_url = sqlite_task.get_async_sqlalchemy_database_url()
async_engine_sqlite_task = create_async_engine(async_sqlalchemy_sqlite_task_database_url)
async_session_sqlite_task = sessionmaker(async_engine_sqlite_task, class_=AsyncSession)

async_sqlalchemy_sqlite_task_data_database_url = sqlite_task_data.get_async_sqlalchemy_database_url()
async_engine_sqlite_task_data = create_async_engine(async_sqlalchemy_sqlite_task_data_database_url)
async_session_sqlite_task_data = sessionmaker(async_engine_sqlite_task_data, class_=AsyncSession)
