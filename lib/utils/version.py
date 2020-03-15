#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import sys

sys.dont_write_bytecode = True

version = sys.version.split()[0]

if version <= "3":
    exit(
        "[-] Incompatible Python version detected ('%s'). For successfully running program you'll have to use version 3.6  (visit 'http://www.python.org/download/')" % version)

extensions = ("gzip", "ssl", "sqlite3", "zlib")

try:
    for _ in extensions:
        __import__(_)

except ImportError:
    errMsg = "Missing one or more core extensions (%s) " % (", ".join("'%s'" % _ for _ in extensions))
    errMsg += "most likely because current version of Python has been "
    errMsg += "built without appropriate dev packages (e.g. 'libsqlite3-dev')"
    exit(errMsg)
