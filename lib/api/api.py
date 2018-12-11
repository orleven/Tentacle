#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import re
import os
import time
import socket
import urllib.error
import http.client
import requests
import tempfile
import contextlib
from lib.core.database import Database
from lib.utils.convert import byte2hex
from lib.utils.convert import jsonize
from lib.utils.convert import dejsonize
from lib.core.data import logger
from lib.core.data import paths
from lib.core.common import get_safe_ex_string
from lib.utils.output import data_to_stdout
from lib.core.settings import RESTAPI_DEFAULT_HOST
from lib.core.settings import RESTAPI_DEFAULT_PORT
from lib.core.settings import RESTAPI_DEFAULT_ADAPTER
from thirdparty.bottle.bottle import error as return_error
from thirdparty.bottle.bottle import get
from thirdparty.bottle.bottle import hook
from thirdparty.bottle.bottle import post
from thirdparty.bottle.bottle import request
from thirdparty.bottle.bottle import response
from thirdparty.bottle.bottle import run
from thirdparty.bottle.bottle import server_names

class DataStore(object):
    admin_id = ""
    current_db = None
    tasks = dict()
    username = None
    password = None

def myserver(host=RESTAPI_DEFAULT_HOST, port=RESTAPI_DEFAULT_PORT, adapter=RESTAPI_DEFAULT_ADAPTER, username=None, password=None):
    """
    REST-JSON API server
    """

    DataStore.admin_id = 'admin_'+ byte2hex(os.urandom(16))
    DataStore.username = username
    DataStore.password = password

    _, Database.filepath = tempfile.mkstemp(prefix="tentacle_", text=False)
    os.close(_)

    if port == 0:  # random
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind((host, 0))
            port = s.getsockname()[1]

    logger.sysinfo("Running REST-JSON API server at '%s:%d'.." % (host, port))
    logger.sysinfo("Admin ID: %s" % DataStore.admin_id)
    logger.sysinfo("IPC database: '%s'" % Database.filepath)

    # Initialize IPC database
    DataStore.current_db = Database(os.path.join(paths.DATA_PATH, 'storage'))
    DataStore.current_db.connect()
    DataStore.current_db.init()


    # Run RESTful API
    try:
        # Supported adapters: aiohttp, auto, bjoern, cgi, cherrypy, diesel, eventlet, fapws3, flup, gae, gevent, geventSocketIO, gunicorn, meinheld, paste, rocket, tornado, twisted, waitress, wsgiref
        # Reference: https://bottlepy.org/docs/dev/deployment.html || bottle.server_names
        if adapter == "gevent":
            from gevent import monkey
            monkey.patch_all()
        elif adapter == "eventlet":
            import eventlet
            eventlet.monkey_patch()
        logger.debug("Using adapter '%s' to run bottle" % adapter)
        run(host=host, port=port, quiet=True, debug=True, server=adapter)
    except socket.error as ex:
        if "already in use" in get_safe_ex_string(ex):
            logger.error("Address already in use ('%s:%s')" % (host, port))
        else:
            raise
    except ImportError:
        if adapter.lower() not in server_names:
            errMsg = "Adapter '%s' is unknown. " % adapter
            errMsg += "(Note: available adapters '%s')" % ', '.join(sorted(server_names.keys()))
        else:
            errMsg = "Server support for adapter '%s' is not installed on this system " % adapter
            errMsg += "(Note: you can try to install it with 'sudo apt-get install python-%s' or 'sudo pip install %s')" % (adapter, adapter)
        logger.error(errMsg)


def myclient(host=RESTAPI_DEFAULT_HOST, port=RESTAPI_DEFAULT_PORT, username=None, password=None):
    """
    REST-JSON API client
    """

    DataStore.username = username
    DataStore.password = password

    dbgMsg = "Example client access from command line:"
    dbgMsg += "\n\t$ taskid=$(curl http://%s:%d/task/new 2>1 | grep -o -I '[a-f0-9]\{16\}') && echo $taskid" % (host, port)
    dbgMsg += "\n\t$ curl -H \"Content-Type: application/json\" -X POST -d '{\"url\": \"http://testphp.vulnweb.com/artists.php?artist=1\"}' http://%s:%d/scan/$taskid/start" % (host, port)
    dbgMsg += "\n\t$ curl http://%s:%d/scan/$taskid/data" % (host, port)
    dbgMsg += "\n\t$ curl http://%s:%d/scan/$taskid/log" % (host, port)
    logger.debug(dbgMsg)

    addr = "http://%s:%d" % (host, port)
    logger.info("Starting REST-JSON API client to '%s'..." % addr)

    try:
        _client(addr)
    except Exception as ex:
        if not isinstance(ex, urllib.error.HTTPError) or ex.code == httplib.UNAUTHORIZED:
            errMsg = "There has been a problem while connecting to the "
            errMsg += "REST-JSON API server at '%s' " % addr
            errMsg += "(%s)" % ex
            logger.critical(errMsg)
            return

    taskid = None
    logger.info("Type 'help' or '?' for list of available commands")

    while True:
        try:
            command = input("api%s> " % (" (%s)" % taskid if taskid else "")).strip()
            command = re.sub(r"\A(\w+)", lambda match: match.group(1).lower(), command)
        except (EOFError, KeyboardInterrupt):
            logger.error("aa error")
            break

        if command in ("data", "log", "status", "stop", "kill"):
            if not taskid:
                logger.error("No task ID in use")
                continue
            raw = _client("%s/scan/%s/%s" % (addr, taskid, command))
            res = dejsonize(raw)
            if not res["success"]:
                logger.error("Failed to execute command %s" % command)
            data_to_stdout("%s\n" % raw)

        elif command.startswith("option"):
            if not taskid:
                logger.error("No task ID in use")
                continue
            try:
                command, option = command.split(" ")
            except ValueError:
                raw = _client("%s/option/%s/list" % (addr, taskid))
            else:
                options = {"option": option}
                raw = _client("%s/option/%s/get" % (addr, taskid), options)
            res = dejsonize(raw)
            if not res["success"]:
                logger.error("Failed to execute command %s" % command)
            data_to_stdout("%s\n" % raw)

        elif command.startswith("new"):
            if ' ' not in command:
                logger.error("Program arguments are missing")
                continue

            try:
                argv = ["sqlmap.py"] + shlex.split(command)[1:]
            except Exception as ex:
                logger.error("Error occurred while parsing arguments ('%s')" % ex)
                taskid = None
                continue

            try:
                cmdLineOptions = cmdLineParser(argv).__dict__
            except:
                taskid = None
                continue

            for key in list(cmdLineOptions):
                if cmdLineOptions[key] is None:
                    del cmdLineOptions[key]

            raw = _client("%s/task/new" % addr)
            res = dejsonize(raw)
            if not res["success"]:
                logger.error("Failed to create new task")
                continue
            taskid = res["taskid"]
            logger.info("New task ID is '%s'" % taskid)

            raw = _client("%s/scan/%s/start" % (addr, taskid), cmdLineOptions)
            res = dejsonize(raw)
            if not res["success"]:
                logger.error("Failed to start scan")
                continue
            logger.info("Scanning started")

        elif command.startswith("use"):
            taskid = (command.split()[1] if ' ' in command else "").strip("'\"")
            if not taskid:
                logger.error("Task ID is missing")
                taskid = None
                continue
            elif not re.search(r"\A[0-9a-fA-F]{16}\Z", taskid):
                logger.error("Invalid task ID '%s'" % taskid)
                taskid = None
                continue
            logger.info("Switching to task ID '%s' " % taskid)

        elif command in ("list", "flush"):
            raw = _client("%s/admin/%s/%s" % (addr, taskid or 0, command))
            res = dejsonize(raw)
            if not res["success"]:
                logger.error("Failed to execute command %s" % command)
            elif command == "flush":
                taskid = None
            data_to_stdout("%s\n" % raw)

        elif command in ("exit", "bye", "quit", 'q'):
            return

        elif command in ("help", "?"):
            msg =  "help           Show this help message\n"
            msg += "new ARGS       Start a new scan task with provided arguments (e.g. 'new -u \"http://testphp.vulnweb.com/artists.php?artist=1\"')\n"
            msg += "use TASKID     Switch current context to different task (e.g. 'use c04d8c5c7582efb4')\n"
            msg += "data           Retrieve and show data for current task\n"
            msg += "log            Retrieve and show log for current task\n"
            msg += "status         Retrieve and show status for current task\n"
            msg += "option OPTION  Retrieve and show option for current task\n"
            msg += "options        Retrieve and show all options for current task\n"
            msg += "stop           Stop current task\n"
            msg += "kill           Kill current task\n"
            msg += "list           Display all tasks\n"
            msg += "flush          Flush tasks (delete all tasks)\n"
            msg += "exit           Exit this client\n"

            data_to_stdout(msg)

        elif command:
            logger.error("Unknown command '%s'" % command)

def _client(url, options=None):
    logger.debug("Calling %s" % url)
    try:
        data = None
        if options is not None:
            data = jsonize(options)
        headers = {"Content-Type": "application/json"}

        if DataStore.username or DataStore.password:
            headers["Authorization"] = "Basic %s" % ("%s:%s" % (DataStore.username or "", DataStore.password or "")).encode("base64").strip()

        res = requests.post(url, data, headers)
        text = res.text
    except:
        if options:
            logger.error("Failed to load and parse %s" % url)
        raise
    return text


@hook('before_request')
def check_authentication():
    if not any((DataStore.username, DataStore.password)):
        return

    authorization = request.headers.get("Authorization", "")
    match = re.search(r"(?i)\ABasic\s+([^\s]+)", authorization)

    if not match:
        request.environ["PATH_INFO"] = "/error/401"

    try:
        creds = match.group(1).decode("base64")
    except:
        request.environ["PATH_INFO"] = "/error/401"
    else:
        if creds.count(':') != 1:
            request.environ["PATH_INFO"] = "/error/401"
        else:
            username, password = creds.split(':')
            if username.strip() != (DataStore.username or "") or password.strip() != (DataStore.password or ""):
                request.environ["PATH_INFO"] = "/error/401"

@hook("after_request")
def security_headers(json_header=True):
    """
    Set some headers across all HTTP responses
    """
    response.headers["Server"] = "Server"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Pragma"] = "no-cache"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Expires"] = "0"

    if json_header:
        response.content_type = "application/json; charset=UTF-8"


@return_error(401)  # Access Denied
def error401(error=None):
    security_headers(False)
    return "Access denied"

@return_error(404)  # Not Found
def error404(error=None):
    security_headers(False)
    return "Nothing here"

@return_error(405)  # Method Not Allowed (e.g. when requesting a POST method via GET)
def error405(error=None):
    security_headers(False)
    return "Method not allowed"

@return_error(500)  # Internal Server Error
def error500(error=None):
    security_headers(False)
    return "Internal server error"

@get('/error/401')
def path_401():
    response.status = 401
    return response