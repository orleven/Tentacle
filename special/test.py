#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author = 'orleven'

'''
This is a example for script
'''

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.name = 'Vul Name'
        self.keyword ='Vul Name'
        self.info = 'Vul Info'
        self.type = 'RCE'
        self.level = 'High'
        self.script_type = ''
        self.server_type = SERVER_PORT_MAP.WEB
        Script.__init__(self,target=target,server_type=self.server_type)

    def prove(self):
        import random
        test = random.randint(1, 100)
        if test > 66:
            self.flag = 1
            self.req.append({"test": test})
            self.res.append({"info": test, "key": "test"})
            self.other = {}
        elif test > 33:
            self.flag = 0
        else:
            pass



