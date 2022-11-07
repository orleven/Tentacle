#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from importlib import reload
from importlib import import_module
from importlib.util import find_spec
from lib.core.g import log

def import_script_file(script_file=None):
    """载入script"""

    try:
        module_spec = find_spec(script_file)
    except:
        log.error(f'Error load script, script: {script_file}, error: module spec error')
    else:
        if module_spec:
            try:
                module = import_module(script_file)
                module = reload(module)
                if 'Script' not in dir(module):
                    log.error(f'Error import script file, script: {script_file}, error: can\'t find Script class.')
                else:
                    return module
            except Exception as e:
                log.error(f'Error import script file, script: {script_file}, error: {str(e)}')
        else:
            log.error(f'Error import script file, script: {script_file}, error: module spec error')
    return None
