#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

import re
from lib.core.env import *
from lib.core.g import log
from lib.core.g import conf
from lib.util.scriptutil import import_script_file
from lib.register import BaseRegister

class ScriptRegister(BaseRegister):
    """
    ScriptRegister
    """

    def __init__(self):

        self.module_name_list = []
        self.module_list = []
        self.func_name = 'prove'
        self.parameter = {}

    def parser_module_name(self, input):
        module_name_list = []
        _len = len(ROOT_PATH) + 1
        # -m *
        if input == '*':
            for parent, dirnames, filenames in os.walk(VUL_SCRIPT_PATH, followlinks=True):
                for each in filenames:
                    if '.py' in each and '__init__' not in each:
                        file_path = os.path.join(parent, each)
                        module_name_list.append('.'.join(re.split('[\\\\/]', file_path[_len:-3])))

        # -m test,./script/test.py,@www
        else:
            for _module in input.split(','):
                # @www
                if _module.startswith("@"):
                    _module = _module[1:]
                    if _module in [SPECIAL, TEST, VUL, INFO]:
                        path = os.path.join(SCRIPT_PATH, _module)
                    else:
                        path = os.path.join(VUL_SCRIPT_PATH, _module)
                    for parent, dirnames, filenames in os.walk(path, followlinks=True):
                        for each in filenames:
                            if '.py' in each and '__init__' not in each:
                                file_path = os.path.join(parent, each)
                                module_name_list.append('.'.join(re.split('[\\\\/]', file_path[_len:-3])))

                # "-m ./script/test.py"
                else:
                    if not _module.endswith('.py'):
                        _module += '.py'

                    _path = os.path.abspath(os.path.join(ROOT_PATH, _module))

                    if os.path.isfile(_path):
                        module_name_list.append('.'.join(re.split('[\\\\/]', _path[_len:-3])))
                    else:
                        msg = f'Module is\'t exist: {_module} ({_path})'
                        log.error(msg)

        if len(module_name_list) == 0:
            log.error("Module is null")
        return module_name_list

    def register_module_name(self):

        if not conf.scan.module:
            conf.scan.module = '*'

        log.debug(f"Set module: {conf.scan.module}")
        module_name_list = self.parser_module_name(conf.scan.module)

        if conf.scan.exclude_module:
            log.debug("Set Exclude module: %s" % conf.scan.exclude_module)
            exclude_module_name_list = self.parser_module_name(conf.scan.exclude_module)
        else:
            exclude_module_name_list = []

        for exclude_module_name in exclude_module_name_list:
            if exclude_module_name in module_name_list:
                module_name_list.remove(exclude_module_name)

        self.module_name_list = module_name_list
        return self.module_name_list

    def register_function(self):
        if conf.scan.function:
            if conf.scan.function.startswith('_'):
                log.error(f"Function Invalid: {conf.scan.function}")
                sys.exit(0)
            self.func_name = conf.scan.function
        else:
            self.func_name = 'prove'
        log.debug(f"Set function: {conf.scan.function}")
        return self.func_name

    def register_parameter(self):

        if conf.scan.parameter:
            self.parameter = {}
            if conf.scan.parameter:
                try:
                    parameter_list = conf.scan.parameter.split('&')
                    for parameter in parameter_list:
                        key, value = parameter.split('=')
                        self.parameter[key] = value
                except:
                    msg = 'The parameter input error, please check your input e.g. -p "userlist=user.txt", and you should make sure the module\'s function need the parameter. '
                    log.error(msg)
                    sys.exit(0)
            else:
                self.parameter = {}
            log.debug(f"Set parameter: {conf.scan.parameter}")
        else:
            self.parameter = {}

        return self.parameter


    def register_module(self):

        if len(self.module_name_list) < 0:
            msg = 'Can\'t find any modules. Please check you input.'
            log.error(msg)
            sys.exit(0)

        elif len(self.module_name_list) == 1:
            log.info(f'Loading modual: {self.module_name_list[0]}')
            module = import_script_file(self.module_name_list[0])

            if module == None:
                log.error("Invalid script, Please check the script: %s" % self.module_name_list[0])
                sys.exit(0)

            if self.func_name.lower() in ['show', 'help'] and module:
                if hasattr(module, "Script"):
                    poc = module.Script()
                    msg = "Show Script's Infomation:"
                    msg += "\r\n ------------------------------- "
                    msg += "\r\n| Name: " + str(poc.name if 'name' in poc.__dict__ else 'unknown')
                    msg += "\r\n| Keyword: " + str(poc.keyword if 'keyword' in poc.__dict__ else ['unknown'])
                    msg += "\r\n| Infomation: " + str(
                        poc.info if 'info' in poc.__dict__ else 'Unknown Script, please set the infomation for me.')
                    msg += "\r\n| Level: " + str(poc.level if 'level' in poc.__dict__ else 'unknown')
                    msg += "\r\n| Refer: " + str(poc.refer if 'refer' in poc.__dict__ else None)
                    msg += "\r\n| Type: " + str(poc.type if 'type' in poc.__dict__ else 'unknown')
                    msg += "\r\n| Repaire: " + str(poc.repaire if 'repaire' in poc.__dict__ else 'unknown')
                    msg += "\r\n| Default Port: " + str(poc.service_type if 'service_type' in poc.__dict__ else 'unknown')
                    msg += "\r\n ------------------------------- "
                    log.info(msg)
                sys.exit(0)

            self.module_list.append(module)

        else:
            module_list = []
            log.info('Loading modual list...')

            self.module_name_list = list(set(self.module_name_list))

            for module_name in self.module_name_list:
                module = import_script_file(module_name)

                if module == None:
                    log.error(f"Invalid script, Please check the script: {module_name}")
                    continue

                module_list.append(module)

                if len(self.module_list) > 1 and self.func_name.lower() in ['show', 'help']:
                    log.error('Can\'t show so many modules.')
                    sys.exit(0)

            # sort
            self.module_list = list(set(module_list))

    def show(self):
        _len = len(ROOT_PATH) + 1
        log.info('There are available modules as follows:')
        log.info('----------------------------------------------------------------')
        for parent, dirnames, filenames in os.walk(SCRIPT_PATH, followlinks=True):
            if '.git' in parent:
                continue

            for each in filenames:
                if '__init__' in each or each.startswith('.') or 'README' in each:
                    continue
                file_path = os.path.join(parent, each)
                log.info('| {: <60} |'.format(file_path[_len:-3]))
        log.info('----------------------------------------------------------------')


    async def load_script(self):
        for module in self.module_list:
            yield module

    async def load_module(self):
        if len(self.module_list) == 0:
            self.register_module_name()
            self.register_module()
            self.register_function()
            self.register_parameter()


    def load_module_by_name(self, module_name=None):
        if module_name:
            module = import_script_file(module_name)
            if module:
                self.register_function()
                self.register_parameter()
                return module
            else:
                log.error(f"Invalid script, Please check the script: {module_name}")
                return None
        return None

