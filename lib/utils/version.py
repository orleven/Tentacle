#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'


import sys

version = sys.version.split()[0]

if version <= "3" :
    exit("[CRITICAL] incompatible Python version detected ('%s'). For successfully running program you'll have to use version 3.x  (visit 'http://www.python.org/download/')" % version)

extensions = ("gzip", "ssl", "sqlite3", "zlib")

try:
    for _ in extensions:
        __import__(_)
except ImportError:
    errMsg = "missing one or more core extensions (%s) " % (", ".join("'%s'" % _ for _ in extensions))
    errMsg += "most likely because current version of Python has been "
    errMsg += "built without appropriate dev packages (e.g. 'libsqlite3-dev')"
    exit(errMsg)