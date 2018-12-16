#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.core.datatype import AttribDict

from lib.core.log import logger

paths = AttribDict()

logger = logger()

engine = None

conf = AttribDict()
#
# object to share within function and classes results
kb = AttribDict()
#
# # object with each database management system specific queries
# # queries = {}




