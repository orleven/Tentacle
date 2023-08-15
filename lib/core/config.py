#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author: orleven

from lib.core.env import *
import json
import configparser
from attribdict import AttribDict

def config_parser():
    """解析配置文件，如不存在则创建"""

    if not os.path.exists(CONFIG_FILE_PATH):
        init_conf(CONFIG_FILE_PATH)
        exit(f"Please set the {PROJECT_NAME} config in {CONFIG_FILE_PATH}...")

    config = load_conf(CONFIG_FILE_PATH)
    return config


def load_conf(path):
    """加载配置文件"""

    config = AttribDict()
    cf = configparser.ConfigParser()
    cf.read(path)
    sections = cf.sections()
    for section in sections:
        config[section] = AttribDict()
        for option in cf.options(section):
            value = cf.get(section, option)
            try:
                if value.startswith("{") and value.endswith("}") or value.startswith("[") and value.endswith("]"):
                    value = json.loads(value)
                elif value.lower() == "false":
                    value = False
                elif value.lower() == "true":
                    value = True
                else:
                    value = int(value)
            except Exception as e:
                pass
            config[section][option] = value
    return config


def init_conf(path):
    """初始化配置文件"""

    if not os.path.exists(CONFIG_PATH):
        os.mkdir(CONFIG_PATH)

    configs = {
        ("basic", f"This is a basic config for {PROJECT_NAME}"): {

        },
        ("scan", f"This is a scan config for {PROJECT_NAME}"): {
            ("scan_timeout", "Connection timeout"): 5,
            ("scan_headers", '{"User-Agent": f"This is a Test UA."}'): '',
            ("max_task_num", ""): 100,
            ("scan_max_retries", ""): 0,
            ("scan_dict_path", ""): DICT,
        },
        ("proxy", f"This is a proxy config for {PROJECT_NAME}"): {
            ("proxy", ""): False,
            ("proxy_url", ""): "socks5://127.0.0.1:1080",
        },
        ("dnslog", f"This is a dnslog config for {PROJECT_NAME}"): {
            ("dnslog_top_domain", ""): "dnslog.com",
            ("dnslog_api_url", ""): "https://api.dnslog.com/dnslog/list",
            ("dnslog_api_key", ""): "dnslog_api_key",
        },
        ("fofa", f"This is a fofa config for {PROJECT_NAME}"): {
            ("email", ""): "email",
            ("token", ""): "token",
        },
        ("zoomeye", f"This is a zoomeye config for {PROJECT_NAME}"): {
            ("username", ""): "username",
            ("password", ""): "password",
        },
        ("shadon", f"This is a shadon config for {PROJECT_NAME}"): {
            ("token", ""): "token",
        },
        ("google", f"This is a fofa config for {PROJECT_NAME}"): {
            ("developer_key", ""): "developer_key",
            ("search_enging", ""): "search_enging",
        },
        ("github", f"This is a github config for {PROJECT_NAME}"): {
            ("token1", ""): "token1",
            ("token2", ""): "token2",
            ("token3", ""): "token3",
            ("token4", ""): "token4",
        },
    }

    cf = configparser.ConfigParser(allow_no_value=True)
    for (section, section_comment), section_value in configs.items():
        cf.add_section(section)

        if section_comment and section_comment != "":
            cf.set(section, fix_comment_content(f"{section_comment}\r\n"))

        for (key, key_comment), key_value in section_value.items():
            if key_comment and key_comment != "":
                cf.set(section, fix_comment_content(key_comment))
            if isinstance(key_value, dict) or isinstance(key_value, list):
                key_value = json.dumps(key_value)
            else:
                key_value = str(key_value)
            cf.set(section, key, f"{key_value}\r\n")

    with open(path, 'w+') as configfile:
        cf.write(configfile)


def fix_comment_content(content):
    """按照80个字符一行就行格式化处理"""

    text = f'; '
    for i in range(0, len(content)):
        if i != 0 and i % 80 == 0:
            text += '\r\n; '
        text += content[i]
    return text