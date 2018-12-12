# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @author: 'orleven'
#
# import os
# import time
# import socket
# import tempfile
# import contextlib
# from lib.core.subprocessng import Popen
# from lib.core.datatype import AttribDict
# from lib.api.database import Database
# from lib.utils.cipher import md5
# from lib.utils.convert import byte2hex
# from lib.core.options import init_options
# from lib.core.engine import Engine
# from lib.core.module import load_module,load_target
# from lib.core.data import logger
# from lib.core.data import engine
# from lib.core.enums import MKSTEMP_PREFIX
# from lib.utils.message import getSafeExString
# from lib.core.settings import RESTAPI_DEFAULT_HOST
# from lib.core.settings import RESTAPI_DEFAULT_PORT
# from lib.core.settings import RESTAPI_DEFAULT_ADAPTER
# from thirdparty.bottle.bottle import server_names
# from thirdparty.bottle.bottle import run
#
# class Task(object):
#     def __init__(self, taskid, remote_addr):
#         self.remote_addr = remote_addr
#         self.process = None
#         self.output_directory = None
#         self.options = None
#         self._original_options = None
#         self.initialize_options(taskid)
#
#     def initialize_options(self, taskid):
#         datatype = {"boolean": False, "string": None, "integer": None, "float": None}
#         self.options = AttribDict()
#
#         for _ in optDict:
#             for name, type_ in optDict[_].items():
#                 type_ = unArrayizeValue(type_)
#                 self.options[name] = _defaults.get(name, datatype[type_])
#
#         # Let sqlmap engine knows it is getting called by the API,
#         # the task ID and the file path of the IPC database
#         self.options.api = True
#         self.options.taskid = taskid
#         self.options.database = Database.filepath
#
#         # Enforce batch mode and disable coloring and ETA
#         self.options.batch = True
#         self.options.disableColoring = True
#         self.options.eta = False
#
#         self._original_options = AttribDict(self.options)
#
#     def set_option(self, option, value):
#         self.options[option] = value
#
#     def get_option(self, option):
#         return self.options[option]
#
#     def get_options(self):
#         return self.options
#
#     def reset_options(self):
#         self.options = AttribDict(self._original_options)
#
#     def engine_start(self):
#         handle, configFile = tempfile.mkstemp(prefix=MKSTEMP_PREFIX.CONFIG, text=True)
#         os.close(handle)
#         saveConfig(self.options, configFile)
#
#         if os.path.exists("sqlmap.py"):
#             self.process = Popen(["python", "sqlmap.py", "--api", "-c", configFile], shell=False, close_fds=not IS_WIN)
#         elif os.path.exists(os.path.join(os.getcwd(), "sqlmap.py")):
#             self.process = Popen(["python", "sqlmap.py", "--api", "-c", configFile], shell=False, cwd=os.getcwd(), close_fds=not IS_WIN)
#         else:
#             self.process = Popen(["sqlmap", "--api", "-c", configFile], shell=False, close_fds=not IS_WIN)
#
#     def engine_stop(self):
#         if self.process:
#             self.process.terminate()
#             return self.process.wait()
#         else:
#             return None
#
#     def engine_process(self):
#         return self.process
#
#     def engine_kill(self):
#         if self.process:
#             try:
#                 self.process.kill()
#                 return self.process.wait()
#             except:
#                 pass
#         return None
#
#     def engine_get_id(self):
#         if self.process:
#             return self.process.pid
#         else:
#             return None
#
#     def engine_get_returncode(self):
#         if self.process:
#             self.process.poll()
#             return self.process.returncode
#         else:
#             return None
#
#     def engine_has_terminated(self):
#         return isinstance(self.engine_get_returncode(), int)