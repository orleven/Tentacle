#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from lib.core.env import *

class SQLite(object):

    def __init__(self, dbname=None):
        self.dbname = dbname
        self.async_sqlalchemy_database_url = f'sqlite+aiosqlite:///{DATA_PATH}/{self.dbname}'

    def get_async_sqlalchemy_database_url(self):
        """Async 使用"""

        return self.async_sqlalchemy_database_url
