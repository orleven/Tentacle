#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

import os
import re
import sys
import glob
import importlib.util
from lib.core.data import conf
from lib.core.data import logger
from lib.core.data import paths
from lib.core.common import get_safe_ex_string

class POCManager:

    def __init__(self, input_module, input_func, input_parameter):
        self.modules_name = None
        self.func_name = None
        self.parameter = None
        if conf['show']:
            self.show()
        self._module_register(input_module)
        self._function_register(input_func)
        self._parameter_register(input_parameter)
        self.modules = []

    def show(self):
        _len = len(paths.ROOT_PATH) + 1
        msg = 'There are available modules as follows: \r\n'
        msg += '-----------------------------------------------------------\r\n'
        msg += '| {: <55} |\r\n'.format('Module path, you can load module by -m module_path,')
        msg += '| {: <55} |\r\n'.format('and you can see module\' description for -f show')
        msg += '-----------------------------------------------------------\r\n'
        for parent, dirnames, filenames in os.walk(paths.SCRIPT_PATH, followlinks=True):
            for each in filenames:
                if '__init__' in each:
                    continue
                file_path = os.path.join(parent, each)
                msg += '| {: <55} |\r\n'.format(file_path[_len:-3])
                # import importlib.util
                # module_name = '.'.join(re.split('[\\\\/]',file_path[_len:-3]))
                # module_spec = importlib.util.find_spec(module_name)
                # if module_spec:
                # module = importlib.import_module(module_name)
                # from inspect import getmembers, isfunction
                # fun= [_fun[0] for _fun in getmembers(module) if isfunction(_fun[1]) and '_' not in _fun[0]]
                # doc = module.__doc__ if module.__doc__ !=None else ''
                # msg += '| {: <50} | {:<} \r\n'.format(file_path[_len:-3], doc )
        msg += '-----------------------------------------------------------\r\n'
        sys.exit(logger.sysinfo(msg))

    def _module_register(self, input_module):
        _len = len(paths.ROOT_PATH) + 1

        if not input_module:
            msg = 'Use -m to load module. Example: [-m test] or [-m ./script/test.py] or [-m @thinkphp], and you can see all module name by --show.'
            sys.exit(logger.error(msg))

        modules = []

        # -m *
        if input_module == '*':
            for parent, dirnames, filenames in os.walk(paths.SCRIPT_PATH, followlinks=True):
                if len(filenames) == 0:
                    msg = 'Module [%s] is null.' % paths.SCRIPT_PATH
                    logger.error(msg)

                for each in filenames:
                    if '__init__' in each:
                        continue
                    file_path = os.path.join(parent, each)
                    modules.append('.'.join(re.split('[\\\\/]', file_path[_len:-3])))
        else:
            # -m test,./script/test.py,@www
            for _module in input_module.split(','):

                # @www
                if _module.startswith("@"):
                    if _module[1:] == 'special':
                        _path = os.path.join(paths.SPECIAL_SCRIPT_PATH, _module[1:], '*.py')
                    else:
                        _path = os.path.join(paths.SCRIPT_PATH, _module[1:], '*.py')

                    module_name_list = glob.glob(_path)

                    if len(module_name_list) == 0:
                        msg = 'Module is not exist: %s (%s)' % (_module, _path)
                        logger.error(msg)
                    else:
                        for each in module_name_list:
                            if '__init__' in each:
                                continue
                            modules.append('.'.join(re.split('[\\\\/]', each[_len:-3])))

                else:
                    if not _module.endswith('.py'):
                        _module += '.py'

                    # handle input: "-m ./script/test.py"
                    if os.path.split(_module)[0]:
                        _path = os.path.abspath(os.path.join(paths.ROOT_PATH, _module))

                    # handle input: "-m test"  "-m test.py"
                    else:
                        _path = os.path.abspath(os.path.join(paths.SCRIPT_PATH, _module))

                    if os.path.isfile(_path):
                        modules.append('.'.join(re.split('[\\\\/]', _path[_len:-3])))
                    else:
                        msg = 'Module is\'t exist: %s (%s)' % (_module, _path)
                        logger.error(msg)

        self.modules_name = modules
        logger.debug("Set module: %s" % input_module)
        return self.modules_name

    def load(self):

        if len(self.modules_name) < 0:
            msg = 'Can\'t find any modules. Please check you input.'
            sys.exit(logger.error(msg))

        elif len(self.modules_name) == 1:
            logger.sysinfo('Loading modual: %s' % (self.modules_name[0]))
            module = self._load_module(self.modules_name[0])

            if module == None:
                logger.error("Invalid POC script, Please check the script: %s" %self.modules_name[0])
                sys.exit()

            if self.func_name.lower() in ['show','help'] and module:
                poc = module.POC()
                msg = "Show POC's Infomation:"
                msg += "\r\n ------------------------------- "
                msg += "\r\n| Name: " + str(poc.name if 'name' in poc.__dict__ else 'unknown')
                msg += "\r\n| Keyword: " + str(poc.keyword if 'keyword' in poc.__dict__ else ['unknown'])
                msg += "\r\n| Infomation: " + str(poc.info if 'info' in poc.__dict__ else 'Unknown POC, please set the infomation for me.')
                msg += "\r\n| Level: " + str(poc.level if 'level' in poc.__dict__ else 'unknown')
                msg += "\r\n| Refer: " + str(poc.refer if 'refer' in poc.__dict__ else None)
                msg += "\r\n| Type: " + str(poc.type if 'type' in poc.__dict__ else 'unknown')
                msg += "\r\n| Repaire: " + str(poc.repaire if 'repaire' in poc.__dict__ else 'unknown')
                msg += "\r\n| Default Port: " + str(poc.service_type if 'service_type' in poc.__dict__ else 'unknown')
                msg += "\r\n ------------------------------- "
                logger.sysinfo(msg)
                sys.exit()

            self.modules.append(module)
            if 'script.info.port_scan' not in self.modules_name:
                module = self._load_module('script.info.port_scan')
                self.modules_name.append('script.info.port_scan')
                self.modules.append(module)
                if module == None:
                    logger.error("Invalid POC script, Please check the script: %s" % self.modules_name[0])
                    sys.exit()

        else:
            modules = []
            logger.sysinfo('Loading moduals...')

            if 'script.info.port_scan' not in self.modules_name:
                self.modules_name.append('script.info.port_scan')

            self.modules_name = list(set(self.modules_name))

            for module_name in self.modules_name:
                module = self._load_module(module_name)

                if module == None:
                    logger.error("Invalid POC script, Please check the script: %s" % module_name)
                    continue

                modules.append(module)

                if len(self.modules) > 1 and self.func_name.lower() in  ['show','help']:
                    sys.exit(logger.error('Can\'t show so many modules.'))

            # sort
            self.modules = sorted(modules, key=lambda modules: modules.POC().priority)

    def _function_register(self ,input_func):
        if input_func:
            if input_func.startswith('_'):
                sys.exit(logger.error("Function Invalid: %s" % input_func))
            self.func_name = input_func
        else:
            self.func_name = 'prove'
        logger.debug("Set function: %s" % input_func)
        return self.func_name

    def _load_module(self,module_name):
        module_spec = importlib.util.find_spec(module_name)

        if module_spec:
            try:
                module = importlib.import_module(module_name)

                if 'POC' not in dir(module):
                    logger.error('Invalid POC script, Please check the script: %s' % module.__name__)
                else:
                    return module
            except Exception as e:
                logger.error('Invalid POC script, Please check the script: %s' % module_name)
                logger.error(get_safe_ex_string(e))
        else:
            logger.error('Can\'t load modual: %s.' % conf.module_path)
        return None

    def _parameter_register(self, input_parameter):
        if input_parameter:
            self.parameter = {}

            if input_parameter != None:
                if 'parameter' in conf.keys():
                    self.parameter = conf['parameter']

                try:
                    datas = input_parameter.split('&')
                    for _data in datas:
                        _key, _value = _data.split('=')
                        self.parameter[_key] = _value
                except:
                    msg = 'The parameter input error, please check your input e.g. -p "userlist=user.txt", and you should make sure the module\'s function need the parameter. '
                    sys.exit(logger.error(msg))
            else:
                self.parameter = {}

            logger.sysinfo("Set parameter: %s" % str(input_parameter))
        else:
            self.parameter = {}

        return self.parameter