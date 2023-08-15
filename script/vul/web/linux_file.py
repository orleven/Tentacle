#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

from lib.util.aiohttputil import ClientSession
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):
    """
    InfoLeakFile
    """

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.WEB

        self.file_dic = {
            # unix
            ".ssh/authorized_keys": "ssh-rsa",
            ".ssh/id_rsa": "----END RSA",
            ".ssh/id_rsa.key": "----END RSA",
            ".ssh/id_rsa.pub": "----END RSA",
            ".ssh/id_rsa.pub~": "----END RSA",
            ".ssh/id_rsa~": "----END RSA",
            ".ssh/known_hosts": "ssh-rsa",
            ".ssh/config": "StrictHostKeyChecking",
            ".babel.json": "\"babelrc\":",
            ".bash_logout": "# ~/.bash_logout",
            ".bash_profile": "export PATH",
            ".bashrc": " /etc/",
            ".eslintrc": "\"babel-eslint\"",
            ".npmrc": "registry=http",
            ".zsh_history": "cd ",
            ".history": "cd ",
            ".bash_history": "cd ",
            ".mysql_history": "use\\040",
            ".viminfo": "This viminfo",
        }

    async def prove(self):
        if self.base_url:
            async with ClientSession() as session:
                for path in self.get_url_normpath_list(self.url):
                    if path[-1] == '/':
                        for file_path, file_keyword in self.file_dic.items():
                            try:
                                url = path + file_path
                                async with session.get(url=url, allow_redirects=False) as res:
                                    if res and res.status == 200:
                                        text_source = await res.text()
                                        text = text_source.lower()
                                        if text and file_keyword.lower() in text.lower():
                                            yield url
                            except:
                                pass
