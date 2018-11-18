#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import re
import sys
import logging
from lib.core.data import kb
from lib.core.data import logger
from lib.core.log import LOGGER_HANDLER
from lib.core.settings import BANNER
from lib.core.settings import IS_WIN
from openpyxl import Workbook
from thirdparty.termcolor.termcolor import colored
from thirdparty.colorama.initialise import init as coloramainit

def banner():
    if IS_WIN:
        coloramainit()
    data_to_stdout(BANNER, force_output=True)


def to_excal(datalines,file,taskname = None):
    filename = file + '.xlsx'
    if taskname:
        logger.info('Task export to %s: %s' % (filename,taskname))
    else:
        logger.info('Task Export to %s...' % (filename))
    book = Workbook()
    ws = book.active
    i = 1
    titleList = []
    for line in datalines:
        # mydic = eval(line.decode('utf-8'))
        i = i + 1
        for key in line:
            if key not in titleList:
                titleList.append(key)
                ws.cell(row=1, column=len(titleList)).value = key
            try:
                if isinstance(line[key], int) or isinstance(line[key], str):
                    ws.cell(row=i, column=titleList.index(key) + 1).value = line[key]
                elif isinstance(line[key], list):
                    ws.cell(row=i, column=titleList.index(key) + 1).value = str(line[key])
                elif isinstance(line[key], dict):
                    ws.cell(row=i, column=titleList.index(key) + 1).value = str(line[key])
                else:
                    ws.cell(row=i, column=titleList.index(key) + 1).value = "Types of printing are not supported."
            except:
                ws.cell(row=i, column=titleList.index(key) + 1).value = "Some error."
    book.save(filename)
    if taskname:
        logger.sysinfo('Task exported to %s successful: %s' % (filename,taskname))
    else:
        logger.sysinfo('Exported to %s successful!' % (filename))

def print_dic(data):
    if 'url' in data.keys() and data['url'] != None and data['url'] != '':
        message = data['url']
    else:
        address = data['target_host'] + ":" + str(data['target_port']) if data['target_port'] != 0 else data[
            'target_host']
        message = address

    if len(data['res']) == 0:
        msg = '[{0}] {1}'.format(data['module_name'], message)
    for res in data['res']:
        info = res['info'] if 'info' in res.keys() else ""
        key = res['key'] if 'key' in res.keys() else ""
        msg = '[{0}] {1}: {2}\t[{3}]'.format(data['module_name'], message, info, key)

    if data['flag'] == 1:
        logger.success(msg)
    elif data['flag'] == -1:
        logger.error(msg)
    else:
        logger.warning(msg)

    # for res in data['res']:
    #     info = res['info'] if 'info' in res.keys() else ""
    #     # for k, v in res.items():
    #     #     print(k, v)
    #     if 'url' in data.keys() and data['url']!=None and data['url']!='':
    #         logger.info(data['url']+'\t'+info)
    #     else:
    #         address = data['target_host']+":"+str(data['target_port']) if data['target_port'] !=0 else data['target_host']
    #         logger.info(address+'\t'+info)


###########################
def single_time_warn_message(message):  # Cross-linked function
    sys.stdout.write(message)
    sys.stdout.write("\n")
    sys.stdout.flush()



def data_to_stdout(data, force_output=False, bold=False, content_type=None):
    """
    Writes text to the stdout (console) stream
    """

    message = ""

    if not kb.get("threadException"):
        pass # ?????
        if force_output :
        # if forceOutput or not getCurrentThreadData().disableStdOut:
            if kb.get("multiThreadMode"):
                logging._acquireLock()
            # print(data)
            # if isinstance(data, str):
            #     message = stdoutencode(data)
            #     print(data)
            # else:
            #     message = data
            message = data
            try:

                sys.stdout.write(set_color(message, bold))
                # if conf.get("api"):
                #     sys.stdout.write(message,  content_type)
                # else:
                #     sys.stdout.write(setColor(message, bold))

                sys.stdout.flush()
            except IOError:
                pass

            if kb.get("multiThreadMode"):
                logging._releaseLock()

            kb.prependFlag = isinstance(data, str) and (len(data) == 1 and data not in ('\n', '\r') or len(data) > 2 and data[0] == '\r' and data[-1] != '\n')

def extract_regex_result(regex, content, flags=0):
    """
    Returns 'result' group value from a possible match with regex on a given
    content

    >>> extract_regex_result(r'a(?P<result>[^g]+)g', 'abcdefg')
    'bcdef'
    """

    retVal = None

    if regex and content and "?P<result>" in regex:
        match = re.search(regex, content, flags)

        if match:
            retVal = match.group("result")

    return retVal

def set_color(message, bold=False):
    retVal = message

    level = extract_regex_result(r"\[(?P<result>[A-Z ]+)\]", message) or kb.get("stickyLevel")

    if message and getattr(LOGGER_HANDLER, "is_tty", False):  # colorizing handler
        if bold:
            retVal = colored(message, color=None, on_color=None, attrs=("bold",))
        elif level:
            level = getattr(logging, level, None) if isinstance(level, str) else level
            _ = LOGGER_HANDLER.level_map.get(level)
            if _:
                background, foreground, bold = _
                retVal = colored(message, color=foreground, on_color="on_%s" % background if background else None, attrs=("bold",) if bold else None)

            kb.stickyLevel = level if message and message[-1] != "\n" else None

    return retVal