#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP

_file_dic = {
    ".babelrc": None,
    ".bash_history": None,
    ".bash_history.php": None,
    ".bash_logout": None,
    ".bash_profile": None,
    ".bashrc": None,
    ".build/": None,
    ".buildpath": None,
    ".builds": None,
    ".bundle": None,
    ".cache/": None,
    ".cfg": None,
    ".composer": None,
    ".conf": None,
    ".config": None,
    ".config.php.swp": None,
    ".env": None,
    ".env.php": None,
    ".env.sample.php": None,
    ".environment": None,
    ".idea/": None,
    ".idea/.name": None,
    ".idea/compiler.xml": None,
    ".idea/copyright/profiles_settings.xml": None,
    ".idea/dataSources.ids": None,
    ".idea/dataSources.local.xml": None,
    ".idea/dataSources.xml": None,
    ".idea/deployment.xml": None,
    ".idea/drush_stats.iml": None,
    ".idea/encodings.xml": None,
    ".idea/misc.xml": None,
    ".idea/modules.xml": None,
    ".idea/scopes/scope_settings.xml": None,
    ".idea/Sites.iml": None,
    ".idea/sqlDataSources.xml": None,
    ".idea/tasks.xml": None,
    ".idea/uiDesigner.xml": None,
    ".idea/vcs.xml": None,
    ".idea/woaWordpress.iml": None,
    ".idea/workspace(2).xml": None,
    ".idea/workspace.xml": None,
    ".idea_modules/": None,
    ".ignore": None,
    ".ignored/": None,
    ".settings/": None,
    ".settings/.jsdtscope": None,
    ".settings/org.eclipse.core.resources.prefs": None,
    ".settings/org.eclipse.php.core.prefs": None,
    ".settings/org.eclipse.wst.common.project.facet.core.xml": None,
    ".settings/org.eclipse.wst.jsdt.ui.superType.container": None,
    ".settings/org.eclipse.wst.jsdt.ui.superType.name": None,
    ".ssh/authorized_keys": None,
    ".ssh/id_rsa": None,
    ".ssh/id_rsa.key": None,
    ".ssh/id_rsa.key~": None,
    ".ssh/id_rsa.priv": None,
    ".ssh/id_rsa.priv~": None,
    ".ssh/id_rsa.pub": None,
    ".ssh/id_rsa.pub~": None,
    ".ssh/id_rsa~": None,
    ".ssh/know_hosts": None,
    ".ssh/know_hosts~": None,
    ".ssh/known_host": None,
    ".ssh/known_hosts": None,
    ".zsh_history": None,
    "services": "?wsdl",
    "axis2/services": "?wsdl",
    ".svn/entries": 'dir',
    ".svn/wc.db": 'sqlite format',
    ".svn/all-wcprops": None,
    "Dockerfile": None,
    ".svn/pristine/": None,
    ".svn/prop-base/": None,
    ".svn/props/": None,
    ".svn/text-base/": None,
    ".svn/text-base/index.php.svn-base": None,
    ".svn/tmp/": None,
    "WEB-INF/web.xml": "<web-app",
    "WEB-INF/applicationContext.xml": None,
    "WEB-INF/config.xml": None,
    "server.xml": None,
    "config/database.yml": None,
    "robots.txt": 'disallow:',
    "application.wadl": None,
    "debug.txt": None,
    "nohup.out": None,
    "build.sh": None,
    ".git": None,
    ".git/HEAD": None,
    ".git/index": 'dirc',
    ".git/config": 'master',
    "README.md": None,
    "README": None,
    ".DS_store": None,
    "WEB-INF/database.propertie": '.driver',
    ".htaccess": 'rewrite',
    "phpinfo.php": 'php.ini',
    "php.php": 'php.ini',
    "info.php": 'php.ini',
    "p.php": 'php.ini',
    'phpmyadmin/index.php' : "phpmyadmin",
    "1.php": None,
    "test.php": None,
    "test.jsp": None,
    "test.jspx": None,
    "test.aspx": None,
    "test.asp": None,
    ".aws/config": None,
    "laravel/.env": None,
    ".htpasswd": None,
    "httpd.conf": None,
    "rsync.sh": None,
    "sync.sh": None,
    "settings.ini": None,
    ".mysql.php.swp": None,
    ".settings.php.swp": None,
    "containers/json": None,
    "jolokia/list": None,
    "evn": None,
    "configprops": None,
    "invoker/JMXInvokerServlet": None,
    "ws_utc/config.do": None,
    "databases.yml": None,
    "schema.yml": None,
    "sqlnet.log": None,
    "private.key": None,
    "id_rsa": None,
    "id_dsa": None,
    "id_dsa.ppk": None,
    ".ssh/id_dsa.pub": None,
    "database.inc": None,
    "common.inc": None,
    "db.inc": None,
    "connect.inc": None,
    "conn.inc": None,
    "sql.inc": None,
    "debug.inc": None,
    "wp-config.inc": None,
    "propel.ini": None,
    "config.ini": None,
    "config/config.ini": None,
    "web.config": None,
    "composer.json": None,
    "composer.lock": None,
    ".rediscli_history": None,
    ".cvsignore": None,
    ".history": None,
    ".mysql_history": None,
    ".log": None,
    ".viminfo": None,
    "access.log": None,
    "error.log": None,
    "debug.log": None,
    "sql.log": None,
}

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'info file'
        self.keyword = ['web']
        self.info = 'info file'
        self.type = 'info'
        self.level = 'low'
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                path_list = list(set([
                    self.url_normpath(self.base_url, '/'),
                    self.url_normpath(self.url, './'),
                    self.url_normpath(self.url, '../'),
                ]))
                for path in path_list:
                    # 404 page
                    # Replace the main factors affecting 404 pages to reduce false positives
                    length1 = length2 = 0
                    fix_length = 50
                    # min_length = 10240
                    async with session.get(url=path+'is_not_exist', allow_redirects=False) as res1:
                        length1 = len((await res1.text()).replace('is_not_exist', '')) if res1 else 0
                    async with session.get(url=path + '.is_not_exist', allow_redirects=False) as res1:
                        length2 = len((await res1.text()).replace('.is_not_exist', '')) if res1 else 0

                    # fix bug, file too large would timeout
                    # read_length = (length1 + length2) * 2 + min_length

                    # burst page:
                    for key in _file_dic.keys():
                        url = path + key
                        async with session.get(url=url, allow_redirects=False) as response:
                            if response != None:
                                if response.status == 200:
                                    # Replace the main factors affecting 404 pages to reduce false positives
                                    text = await response.text()
                                    text = text.replace(key, '')
                                    # text = await response.content.read(read_length)

                                    if _file_dic[key] == None:
                                        length = len(text)
                                        if abs(length-length1) > fix_length and abs(length-length2) > fix_length:
                                            self.flag = 1
                                            self.res.append({"info": url, "key": 'info file'})
                                    else:
                                        text = str(text)
                                        if _file_dic[key] in text.lower():
                                            self.flag = 1
                                            self.res.append({"info": url, "key": 'info file'})
