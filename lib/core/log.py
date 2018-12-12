#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import logging
import os
import sys
import time
from lib.core.enums import CUSTOM_LOGGING

class logger:
    def __init__(self, set_level=CUSTOM_LOGGING.SYSINFO,
                 name=os.path.split(os.path.splitext(sys.argv[0])[0])[-1],
                 log_name=time.strftime("%Y-%m-%d.log", time.localtime()),
                 log_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "log"),
                 use_console=True):

        logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "*")
        logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "+")
        logging.addLevelName(CUSTOM_LOGGING.ERROR, "-")
        logging.addLevelName(CUSTOM_LOGGING.WARNING, "!")
        logging.addLevelName(CUSTOM_LOGGING.DEBUG, "DEBUG")

        self.logger = logging.getLogger(name)
        self.set_level(set_level)

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        self.log_handler = logging.FileHandler(os.path.join(log_path, log_name))
        self.log_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S"))
        self.logger.addHandler(self.log_handler)

        if use_console:
            try:
                from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler
                try:
                    console_handler = ColorizingStreamHandler(sys.stdout)
                    console_handler.level_map[logging.getLevelName("*")] = (None, "white", False)
                    console_handler.level_map[logging.getLevelName("+")] = (None, "green", False)
                    console_handler.level_map[logging.getLevelName("-")] = (None, "red", False)
                    console_handler.level_map[logging.getLevelName("!")] = (None, "yellow", False)
                    console_handler.level_map[logging.getLevelName("DEBUG")] = (None, "cyan", False)
                    self.console_handler = console_handler
                except Exception:
                    self.console_handler = logging.StreamHandler(sys.stdout)
            except ImportError:
                self.console_handler = logging.StreamHandler(sys.stdout)
        else:
            self.console_handler = logging.StreamHandler(sys.stdout)

        self.console_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S"))
        self.logger.addHandler(self.console_handler)

    def set_level(self,set_level):
        self.logger.setLevel(set_level)

    def addHandler(self, hdlr):
        self.logger.addHandler(hdlr)

    def removeHandler(self, hdlr):
        self.logger.removeHandler(hdlr)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)

    def sysinfo(self, msg, *args, **kwargs):
        self.logger.log(CUSTOM_LOGGING.SYSINFO, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.log(CUSTOM_LOGGING.ERROR, msg, *args, **kwargs)

    def success(self, msg, *args, **kwargs):
        self.logger.log(CUSTOM_LOGGING.SUCCESS, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.log(CUSTOM_LOGGING.WARNING, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.log(CUSTOM_LOGGING.DEBUG, msg, *args, **kwargs)


LOGGER_HANDLER = None
LOGGER_FILE_HANDLER = None
#
# try:
#     from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler
#
#     # disableColor = False
#     #
#     # for argument in sys.argv:
#     #     if "disable-col" in argument:
#     #         disableColor = True
#     #         break
#
#     # if disableColor:
#     #     LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
#     # else:
#     #     LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
#         # LOGGER_HANDLER.level_map[logging.getLevelName("Task")] = (None, "cyan", False)
#         # LOGGER_HANDLER.level_map[logging.getLevelName("TRAFFIC OUT")] = (None, "magenta", False)
#         # LOGGER_HANDLER.level_map[logging.getLevelName("TRAFFIC IN")] = ("magenta", None, False)
#     try:
#         LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
#         LOGGER_HANDLER.level_map[logging.getLevelName("*")] = (None, "cyan", False)
#         LOGGER_HANDLER.level_map[logging.getLevelName("+")] = (None, "green", False)
#         LOGGER_HANDLER.level_map[logging.getLevelName("-")] = (None, "red", False)
#         LOGGER_HANDLER.level_map[logging.getLevelName("!")] = (None, "yellow", False)
#         LOGGER_HANDLER.level_map[logging.getLevelName("DEBUG")] = (None, "white", False)
#     except Exception:
#         LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
#
# except ImportError:
#     LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
#
# FORMATTER = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
# LOGGER_HANDLER.setFormatter(FORMATTER)
# LOGGER.addHandler(LOGGER_HANDLER)
#
# log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),'log')
# if not os.path.exists(log_dir):
#     os.mkdir(log_dir)
#
# LOGGER_FILE_HANDLER = logging.handlers.RotatingFileHandler(filename=os.path.join(log_dir,'logs.log'), maxBytes=10*1024*1024)
# LOGGER_FILE_HANDLER.setLevel(logging.INFO)
# LOGGER_FILE_HANDLER.setFormatter(FORMATTER)
# LOGGER.addHandler(LOGGER_FILE_HANDLER)
# LOGGER.setLevel(logging.INFO)
#
#
# class MY_LOGGER:
#     @staticmethod
#     def success(msg):
#         return LOGGER.log(CUSTOM_LOGGING.SUCCESS, msg)
#
#     @staticmethod
#     def info(msg):
#         return LOGGER.log(CUSTOM_LOGGING.SYSINFO, msg)
#
#     @staticmethod
#     def warning(msg):
#         return LOGGER.log(CUSTOM_LOGGING.WARNING, msg)
#
#     @staticmethod
#     def error(msg):
#         return LOGGER.log(CUSTOM_LOGGING.ERROR, msg)
#
#     @staticmethod
#     def critical(msg):
#         return LOGGER.log(CUSTOM_LOGGING.ERROR, msg)
#
#     @staticmethod
#     def debug(msg):
#         return LOGGER.log(CUSTOM_LOGGING.DEBUG, msg)

    # @staticmethod
    # def security_note(msg, k=''):
    #     MY_LOGGER.info(msg)
    #
    # @staticmethod
    # def security_warning(msg, k=''):
    #     MY_LOGGER.warning(msg)
    #
    # @staticmethod
    # def security_hole(msg, k=''):
    #     MY_LOGGER.success(msg)
    #
    # @staticmethod
    # def security_info(msg, k=''):
    #     MY_LOGGER.info(msg)

