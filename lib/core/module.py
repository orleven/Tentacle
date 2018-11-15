#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import sys
import glob
import os
import importlib.util
from thirdparty.IPy import IPy

from lib.core.hashdb import HashDB
from lib.core.data import paths
from lib.core.data import logger
from lib.core.data import conf
# from lib.core.data import engine
from lib.core.data import paths
from lib.core.data import logger
from lib.utils.iputil import build
from lib.utils.iputil import check_host
from lib.utils.iputil import check_ip
from lib.utils.iputil import check_ippool
'''
    py -3 tentacle_x.py -n -m test  -f show
    py -3 tentacle_x.py -n -m test  -f prove
'''
def load_module():
    module_path = conf['module_path']
    module_spec = importlib.util.find_spec(module_path)
    if module_spec:
        logger.info('Load modual: %s' %(module_path))
        module = importlib.import_module(module_path)
        func_name = conf['func_name']
        if func_name.lower() == 'show':
            help(module)
            # logger.info('Show modual: %s: %s' %(module_path,[_name for _name in dir(module) if  _name[0] != '_']))
        elif func_name not in dir(module):
            # if not getattr(module, conf.FUNCTION) :
            logger.error('Can\' load function: %s.%s(). You can use -f show.' % (module_path ,func_name))
        else:
            return module
    else:
        logger.error('Can\' load modual: %s. You can use --show.' % conf.module_path)
    return  False

def load_target(name):
    # engine[name]['engine'].set_port(engine[name]['target_port'])
    if 'target_simple' in engine[name].keys():
        put_target(name, engine[name]['target_simple'])
        logger.info("(%s) Load target: %s"  % (name,engine[name]['target_simple']))
    elif 'target_file' in engine[name].keys():
        for _line in open(engine[name]['target_file'],'r'):
            line = _line.strip()
            if line:
                put_target(name, line)
        logger.info("(%s) Load target: %s" %(name,engine[name]['target_file']))
    elif 'target_network' in engine[name].keys():
        put_target(name, engine[name]['target_network'])
        logger.info("(%s) Load target: %s" %(name,engine[name]['target_network']))
    elif 'target_task' in engine[name].keys():
        hashdb = HashDB(os.path.join(paths.DATA_PATH, engine[name]['target_task']))
        hashdb.connect(name)
        for _row in hashdb.select_all():
            if _row[4] != None  and _row[4] != '':
                put_target(name, _row[4])
            else:
                put_target(name, _row[2]+":"+_row[3])
        logger.info("(%s) Load target: %s" %(name, engine[name]['target_task']))
    else:
        logger.error("(%s) Task exit: 0 target found! Please load target by iS/iN/iF." %name )



def put_target(name,target):
    # http://localhost
    if "http://" in target or "https://" in target:
        engine[name]['engine'].put_target(target)
    else:

        # 192.168.111.1/24
        if '/' in target and check_ippool(target):
            for each in build(target) :
                engine[name]['engine'].put_target(each)

        # 192.168.111.1-192.168.111.3
        elif '-' in target and check_ippool(target):
            _v = target.split('-')
            for each in build(_v[0],_v[1]):
                engine[name]['engine'].put_target(each)

        # 192.168.111.1
        else:
            if ":" in target:
                _v = target.split(':')
                host = _v[0]
                if check_host(host):
                    engine[name]['engine'].put_target(target)
            else:
                if check_host(target):
                    engine[name]['engine'].put_target(target)

    # try:
    #     _list = IPy.IP(target)
    #     for each in _list:
    #         engine[name]['engine'].put_target(each)
    # except Exception as e:
    #     sys.exit(logger.error('Invalid IP/MASK,%s' % e))

# def loadModule():
#     _name = conf.MODULE_NAMES
#     msg = 'Load script: %s' % _name
#     logger.success(msg)
#
#     print(os.path.splitext(_name)[0], [paths.SCRIPT_PATH])
#
#
#     fp, pathname, description = importlib.find_module(os.path.splitext(_name)[0], [paths.SCRIPT_PATH])
#     try:
#         th.module_obj = importlib.load_module("_", fp, pathname, description)
#         for each in ESSENTIAL_MODULE_METHODS:
#             if not hasattr(th.module_obj, each):
#                 errorMsg = "Can't find essential method:'%s()' in current script，Please modify your script/PoC."
#                 sys.exit(logger.error(errorMsg))
#     except ImportError, e:
#         errorMsg = "Your current scipt [%s.py] caused this exception\n%s\n%s" \
#                    % (_name, '[Error Msg]: ' + str(e), 'Maybe you can download this module from pip or easy_install')
#         sys.exit(logger.error(errorMsg))