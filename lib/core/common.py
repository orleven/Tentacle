#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

from lib.utils.cipher import base64pickle
from lib.utils.cipher import base64unpickle

def serialize_object(object_):
    return base64pickle(object_)

def unserialize_object(value):
    return base64unpickle(value) if value else None


def get_safe_ex_string(ex, encoding=None):
    """
    Safe way how to get the proper exception represtation as a string
    (Note: errors to be avoided: 1) "%s" % Exception(u'\u0161') and 2) "%s" % str(Exception(u'\u0161'))

    >>> get_safe_ex_string(Exception('foobar'))
    u'foobar'
    """

    retVal = ex

    if getattr(ex, "message", None):
        retVal = ex.message
    elif getattr(ex, "msg", None):
        retVal = ex.msg
    return retVal.strip()
    # return getUnicode(retVal or "", encoding=encoding).strip()
