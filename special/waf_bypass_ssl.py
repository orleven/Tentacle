#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

import re, requests, pycurl,urllib.parse,tempfile

from script import Script, SERVER_PORT_MAP

class POC(Script):
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'waf bypass ssl'
        self.keyword = ['waf', 'bypass', 'ssl', 'web']
        self.info = 'waf bypass ssl.'
        self.type = 'info'
        self.level = 'info'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        # from sslscan import ui
        # ui.load_modules()
        # scanner = ui.Scanner()
        # for pro in ["ssl2","ssl3","tls10","tls11","tls12"]:
        #     scanner.config.set_value(pro, True)
        # name, sep, options = 'server.ciphers'.partition(":")
        # scanner.append_load(name, options, base_class=ui.BaseScan)
        # name, sep, options = "term:rating=builtin.0_5".partition(":")
        # scanner.append_load(name, options, base_class=ui.BaseReport)
        # module = scanner.load_handler_from_uri("www.baidu.com")
        # scanner.set_handler(module)
        # scanner.reset_knowledge_base()
        # scanner.run_scans()
        # scanner.run_reports()

        self.get_url()
        if self.base_url:
            cmd = 'pysslscan scan --scan server.ciphers  --scan=server.preferred_ciphers --ssl2 --ssl3 --tls10 --tls11 --tls12 ' + self.target_host
            # cmd = 'sslscan --no-colour --no-heartbleed --show-ciphers --sleep 500 --timeout=45 '+ data['target_host']
            lines = _subprocess(cmd.split())
            lines = lines.strip().split('\n')
            poc = "?&mtestid=1%27%20and%20%271%27$%271"
            ssllist =[]
            for line in lines:
                # line = str(line, 'utf-8')
                if "Accepted" in line or "Preferred" in line:
                    pattern = re.compile('[A-Z\d\_]{5,}')
                    match = pattern.search(line)
                    if match:
                        # TLS_RSA_WITH_AES_128_CBC_SHA
                        # curl --ciphers ecdhe_rsa_aes_256_sha    https://www.baidu.com'
                        ciphers = match.group()
                        if ciphers in _openssl_ssls.keys():
                            ciphers_ciphers = _openssl_ssls[ciphers]
                        elif ciphers in _curl_ssls.keys():
                            ciphers_ciphers = _curl_ssls[ciphers]
                        else:
                            ciphers_ciphers = "-".join(ciphers.split("_")[1:])
                        if ciphers_ciphers not in ssllist:
                            res_status = _curl(self.base_url, ciphers_ciphers, poc)
                            # print("curl --ciphers " + ciphers_ciphers + "  " + base_url + poc, str(res_status))
                            if res_status == 200:
                                self.flag = 1
                                self.req.append({"ssl": ciphers})
                                self.res.append({"key": ciphers + " "+ str(res_status),
                                                    "info": "curl --ciphers " + ciphers_ciphers + "  " + self.base_url + poc})
                            ssllist.append(ciphers_ciphers)

        # code = chardet.detect(waf_ssl)['encoding'] if chardet.detect(waf_ssl)['encoding'] not in ['ISO-8859-5','KOI8-R'] else 'gbk'
        # print(waf_ssl.decode(code)+":"+code)

def _subprocess(cmd):
    import tempfile,subprocess
    rt = ''
    try:

        # 得到一个临时文件对象， 调用close后，此文件从磁盘删除
        out_temp = tempfile.TemporaryFile(mode='w+')
        # 获取临时文件的文件号
        fileno = out_temp.fileno()

        # 执行外部shell命令， 输出结果存入临时文件中
        p = subprocess.Popen(cmd, shell=True, stdout=fileno, stderr=fileno)
        p.wait()

        # 从临时文件读出shell命令的输出结果
        out_temp.seek(0)
        rt = out_temp.read()

        # 以换行符拆分数据，并去掉换行符号存入列表
        # rt_list = rt.strip().split('\n')


    except Exception as e:
        pass
    finally:
        if out_temp:
            out_temp.close()
    return rt


def _curl(url,ciphers,poc):
    try:
        import pycurl, tempfile
    #     out_temp = tempfile.TemporaryFile(mode='w+')
        # fileno = out_temp.fileno()
        c = pycurl.Curl()
        c.setopt(c.URL, url + poc)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.SSL_CIPHER_LIST,ciphers)
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.CONNECTTIMEOUT, 5)
        c.setopt(pycurl.TIMEOUT, 5)
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.PROXY, "127.0.0.1")
        c.setopt(pycurl.PROXYPORT, 7999)
        c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
        with  tempfile.NamedTemporaryFile() as fp:
            c.setopt(pycurl.WRITEHEADER, fp)
            c.setopt(pycurl.WRITEDATA, fp)
            c.perform()
            # out_temp.seek(0)
            # rt = out_temp.read()
        return c.getinfo(pycurl.HTTP_CODE)
    except Exception as e:
        pass


_curl_ssls = {
    "SSL_EN_RC4_128_WITH_MD5": "rc4-md5",
    "SSL_EN_RC4_128_EXPORT40_WITH_MD5": "rc4export",
    "SSL_EN_RC2_128_CBC_WITH_MD5": "rc2",
    "SSL_EN_RC2_128_CBC_EXPORT40_WITH_MD5": "rc2export",
    "SSL_EN_DES_64_CBC_WITH_MD5": "des",
    "SSL_EN_DES_192_EDE3_CBC_WITH_MD5": "desede3",
    "SSL_RSA_WITH_RC4_128_MD5": "rsa_rc4_128_md5",
    "SSL_RSA_WITH_RC4_128_SHA": "rsa_rc4_128_sha",
    "SSL_RSA_WITH_3DES_EDE_CBC_SHA": "rsa_3des_sha",
    "SSL_RSA_WITH_DES_CBC_SHA": "rsa_des_sha",
    "SSL_RSA_EXPORT_WITH_RC4_40_MD5": "rsa_rc4_40_md5",
    "SSL_RSA_EXPORT_WITH_RC2_CBC_40_MD5": "rsa_rc2_40_md5",
    "SSL_RSA_WITH_NULL_MD5": "rsa_null_md5",
    "SSL_RSA_WITH_NULL_SHA": "rsa_null_sha",
    "SSL_RSA_FIPS_WITH_3DES_EDE_CBC_SHA": "fips_3des_sha",
    "SSL_RSA_FIPS_WITH_DES_CBC_SHA": "fips_des_sha",
    "SSL_FORTEZZA_DMS_WITH_FORTEZZA_CBC_SHA": "fortezza",
    "SSL_FORTEZZA_DMS_WITH_RC4_128_SHA": "fortezza_rc4_128_sha",
    "SSL_FORTEZZA_DMS_WITH_NULL_SHA": "fortezza_null",
    "TLS_RSA_EXPORT1024_WITH_DES_CBC_SHA": "rsa_des_56_sha",
    "TLS_RSA_EXPORT1024_WITH_RC4_56_SHA": "rsa_rc4_56_sha",
    "TLS_DHE_DSS_WITH_AES_128_CBC_SHA": "dhe_dss_aes_128_cbc_sha",
    "TLS_DHE_DSS_WITH_AES_256_CBC_SHA": "dhe_dss_aes_256_cbc_sha",
    "TLS_DHE_RSA_WITH_AES_128_CBC_SHA": "dhe_rsa_aes_128_cbc_sha",
    "TLS_DHE_RSA_WITH_AES_256_CBC_SHA": "dhe_rsa_aes_256_cbc_sha",
    "TLS_RSA_WITH_AES_128_CBC_SHA": "rsa_aes_128_sha",
    "TLS_RSA_WITH_AES_256_CBC_SHA": "rsa_aes_256_sha",
    "TLS_ECDH_ECDSA_WITH_NULL_SHA": "ecdh_ecdsa_null_sha",
    "TLS_ECDH_ECDSA_WITH_RC4_128_SHA": "ecdh_ecdsa_rc4_128_sha",
    "TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA": "ecdh_ecdsa_3des_sha",
    "TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA": "ecdh_ecdsa_aes_128_sha",
    "TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA": "ecdh_ecdsa_aes_256_sha",
    "TLS_ECDHE_ECDSA_WITH_NULL_SHA": "ecdhe_ecdsa_null_sha",
    "TLS_ECDHE_ECDSA_WITH_RC4_128_SHA": "ecdhe_ecdsa_rc4_128_sha",
    "TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA": "ecdhe_ecdsa_3des_sha",
    "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA": "ecdhe_ecdsa_aes_128_sha",
    "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA": "ecdhe_ecdsa_aes_256_sha",
    "TLS_ECDH_RSA_WITH_NULL_SHA": "ecdh_rsa_null_sha",
    "TLS_ECDH_RSA_WITH_RC4_128_SHA": "ecdh_rsa_128_sha",
    "TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA": "ecdh_rsa_3des_sha",
    "TLS_ECDH_RSA_WITH_AES_128_CBC_SHA": "ecdh_rsa_aes_128_sha",
    "TLS_ECDH_RSA_WITH_AES_256_CBC_SHA": "ecdh_rsa_aes_256_sha",
    "TLS_ECDHE_RSA_WITH_NULL_SHA": "echde_rsa_null",
    "TLS_ECDHE_RSA_WITH_RC4_128_SHA": "ecdhe_rsa_rc4_128_sha",
    "TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA": "ecdhe_rsa_3des_sha",
    "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA": "ecdhe_rsa_aes_128_sha",
    "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA": "ecdhe_rsa_aes_256_sha",
    "TLS_ECDH_anon_WITH_NULL_SHA": "ecdh_anon_null_sha",
    "TLS_ECDH_anon_WITH_RC4_128_SHA": "ecdh_anon_rc4_128sha",
    "TLS_ECDH_anon_WITH_3DES_EDE_CBC_SHA": "ecdh_anon_3des_sha",
    "TLS_ECDH_anon_WITH_AES_128_CBC_SHA": "ecdh_anon_aes_128_sha",
    "TLS_ECDH_anon_WITH_AES_256_CBC_SHA": "ecdh_anon_aes_256_sha",
    "TLS_RSA_WITH_NULL_SHA256": "rsa_null_sha_256",
    "TLS_RSA_WITH_AES_128_CBC_SHA256": "rsa_aes_128_cbc_sha_256",
    "TLS_RSA_WITH_AES_256_CBC_SHA256": "rsa_aes_256_cbc_sha_256",
    "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256": "dhe_rsa_aes_128_cbc_sha_256",
    "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256": "dhe_rsa_aes_256_cbc_sha_256",
    "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256": "ecdhe_ecdsa_aes_128_cbc_sha_256",
    "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256": "ecdhe_rsa_aes_128_cbc_sha_256",
    "TLS_RSA_WITH_AES_128_GCM_SHA256": "rsa_aes_128_gcm_sha_256",
    "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256": "dhe_rsa_aes_128_gcm_sha_256",
    "TLS_DHE_DSS_WITH_AES_128_GCM_SHA256": "dhe_dss_aes_128_gcm_sha_256",
    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256": "ecdhe_ecdsa_aes_128_gcm_sha_256",
    "TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256": "ecdh_ecdsa_aes_128_gcm_sha_256",
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256": "ecdhe_rsa_aes_128_gcm_sha_256",
    "TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256": "ecdh_rsa_aes_128_gcm_sha_256",
}

# https://testssl.sh/openssl-rfc.mapping.html
_openssl_ssls = {
    "TLS_RSA_WITH_NULL_MD5": "NULL-MD5",
    "TLS_RSA_WITH_NULL_SHA": "NULL-SHA",
    "TLS_RSA_EXPORT_WITH_RC4_40_MD5": "EXP-RC4-MD5",
    "TLS_RSA_WITH_RC4_128_MD5": "RC4-MD5",
    "TLS_RSA_WITH_RC4_128_SHA": "RC4-SHA",
    "TLS_RSA_EXPORT_WITH_RC2_CBC_40_MD5": "EXP-RC2-CBC-MD5",
    "TLS_RSA_WITH_IDEA_CBC_SHA": "IDEA-CBC-SHA",
    "TLS_RSA_EXPORT_WITH_DES40_CBC_SHA": "EXP-DES-CBC-SHA",
    "TLS_RSA_WITH_DES_CBC_SHA": "DES-CBC-SHA",
    "TLS_RSA_WITH_3DES_EDE_CBC_SHA": "DES-CBC3-SHA",
    "TLS_DH_DSS_EXPORT_WITH_DES40_CBC_SHA": "EXP-DH-DSS-DES-CBC-SHA",
    "TLS_DH_DSS_WITH_DES_CBC_SHA": "DH-DSS-DES-CBC-SHA",
    "TLS_DH_DSS_WITH_3DES_EDE_CBC_SHA": "DH-DSS-DES-CBC3-SHA",
    "TLS_DH_RSA_EXPORT_WITH_DES40_CBC_SHA": "EXP-DH-RSA-DES-CBC-SHA",
    "TLS_DH_RSA_WITH_DES_CBC_SHA": "DH-RSA-DES-CBC-SHA",
    "TLS_DH_RSA_WITH_3DES_EDE_CBC_SHA": "DH-RSA-DES-CBC3-SHA",
    "TLS_DHE_DSS_EXPORT_WITH_DES40_CBC_SHA": "EXP-EDH-DSS-DES-CBC-SHA",
    "TLS_DHE_DSS_WITH_DES_CBC_SHA": "EDH-DSS-DES-CBC-SHA",
    "TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA": "EDH-DSS-DES-CBC3-SHA",
    "TLS_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA": "EXP-EDH-RSA-DES-CBC-SHA",
    "TLS_DHE_RSA_WITH_DES_CBC_SHA": "EDH-RSA-DES-CBC-SHA",
    "TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA": "EDH-RSA-DES-CBC3-SHA",
    "TLS_DH_anon_EXPORT_WITH_RC4_40_MD5": "EXP-ADH-RC4-MD5",
    "TLS_DH_anon_WITH_RC4_128_MD5": "ADH-RC4-MD5",
    "TLS_DH_anon_EXPORT_WITH_DES40_CBC_SHA": "EXP-ADH-DES-CBC-SHA",
    "TLS_DH_anon_WITH_DES_CBC_SHA": "ADH-DES-CBC-SHA",
    "TLS_DH_anon_WITH_3DES_EDE_CBC_SHA": "ADH-DES-CBC3-SHA",
    "SSL_FORTEZZA_KEA_WITH_NULL_SHA": "",
    "SSL_FORTEZZA_KEA_WITH_FORTEZZA_CBC_SHA": "",
    "SSL_FORTEZZA_KEA_WITH_RC4_128_SHA": "",
    "TLS_KRB5_WITH_DES_CBC_SHA": "KRB5-DES-CBC-SHA",
    "TLS_KRB5_WITH_3DES_EDE_CBC_SHA": "KRB5-DES-CBC3-SHA",
    "TLS_KRB5_WITH_RC4_128_SHA": "KRB5-RC4-SHA",
    "TLS_KRB5_WITH_IDEA_CBC_SHA": "KRB5-IDEA-CBC-SHA",
    "TLS_KRB5_WITH_DES_CBC_MD5": "KRB5-DES-CBC-MD5",
    "TLS_KRB5_WITH_3DES_EDE_CBC_MD5": "KRB5-DES-CBC3-MD5",
    "TLS_KRB5_WITH_RC4_128_MD5": "KRB5-RC4-MD5",
    "TLS_KRB5_WITH_IDEA_CBC_MD5": "KRB5-IDEA-CBC-MD5",
    "TLS_KRB5_EXPORT_WITH_DES_CBC_40_SHA": "EXP-KRB5-DES-CBC-SHA",
    "TLS_KRB5_EXPORT_WITH_RC2_CBC_40_SHA": "EXP-KRB5-RC2-CBC-SHA",
    "TLS_KRB5_EXPORT_WITH_RC4_40_SHA": "EXP-KRB5-RC4-SHA",
    "TLS_KRB5_EXPORT_WITH_DES_CBC_40_MD5": "EXP-KRB5-DES-CBC-MD5",
    "TLS_KRB5_EXPORT_WITH_RC2_CBC_40_MD5": "EXP-KRB5-RC2-CBC-MD5",
    "TLS_KRB5_EXPORT_WITH_RC4_40_MD5": "EXP-KRB5-RC4-MD5",
    "TLS_PSK_WITH_NULL_SHA": "PSK-NULL-SHA",
    "TLS_DHE_PSK_WITH_NULL_SHA": "DHE-PSK-NULL-SHA",
    "TLS_RSA_PSK_WITH_NULL_SHA": "RSA-PSK-NULL-SHA",
    "TLS_RSA_WITH_AES_128_CBC_SHA": "AES128-SHA",
    "TLS_DH_DSS_WITH_AES_128_CBC_SHA": "DH-DSS-AES128-SHA",
    "TLS_DH_RSA_WITH_AES_128_CBC_SHA": "DH-RSA-AES128-SHA",
    "TLS_DHE_DSS_WITH_AES_128_CBC_SHA": "DHE-DSS-AES128-SHA",
    "TLS_DHE_RSA_WITH_AES_128_CBC_SHA": "DHE-RSA-AES128-SHA",
    "TLS_DH_anon_WITH_AES_128_CBC_SHA": "ADH-AES128-SHA",
    "TLS_RSA_WITH_AES_256_CBC_SHA": "AES256-SHA",
    "TLS_DH_DSS_WITH_AES_256_CBC_SHA": "DH-DSS-AES256-SHA",
    "TLS_DH_RSA_WITH_AES_256_CBC_SHA": "DH-RSA-AES256-SHA",
    "TLS_DHE_DSS_WITH_AES_256_CBC_SHA": "DHE-DSS-AES256-SHA",
    "TLS_DHE_RSA_WITH_AES_256_CBC_SHA": "DHE-RSA-AES256-SHA",
    "TLS_DH_anon_WITH_AES_256_CBC_SHA": "ADH-AES256-SHA",
    "TLS_RSA_WITH_NULL_SHA256": "NULL-SHA256",
    "TLS_RSA_WITH_AES_128_CBC_SHA256": "AES128-SHA256",
    "TLS_RSA_WITH_AES_256_CBC_SHA256": "AES256-SHA256",
    "TLS_DH_DSS_WITH_AES_128_CBC_SHA256": "DH-DSS-AES128-SHA256",
    "TLS_DH_RSA_WITH_AES_128_CBC_SHA256": "DH-RSA-AES128-SHA256",
    "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256": "DHE-DSS-AES128-SHA256",
    "TLS_RSA_WITH_CAMELLIA_128_CBC_SHA": "CAMELLIA128-SHA",
    "TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA": "DH-DSS-CAMELLIA128-SHA",
    "TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA": "DH-RSA-CAMELLIA128-SHA",
    "TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA": "DHE-DSS-CAMELLIA128-SHA",
    "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA": "DHE-RSA-CAMELLIA128-SHA",
    "TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA": "ADH-CAMELLIA128-SHA",
    "TLS_RSA_EXPORT1024_WITH_RC4_56_MD5": "EXP1024-RC4-MD5",
    "TLS_RSA_EXPORT1024_WITH_RC2_CBC_56_MD5": "EXP1024-RC2-CBC-MD5",
    "TLS_RSA_EXPORT1024_WITH_DES_CBC_SHA": "EXP1024-DES-CBC-SHA",
    "TLS_DHE_DSS_EXPORT1024_WITH_DES_CBC_SHA": "EXP1024-DHE-DSS-DES-CBC-SHA",
    "TLS_RSA_EXPORT1024_WITH_RC4_56_SHA": "EXP1024-RC4-SHA",
    "TLS_DHE_DSS_EXPORT1024_WITH_RC4_56_SHA": "EXP1024-DHE-DSS-RC4-SHA",
    "TLS_DHE_DSS_WITH_RC4_128_SHA": "DHE-DSS-RC4-SHA",
    "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256": "DHE-RSA-AES128-SHA256",
    "TLS_DH_DSS_WITH_AES_256_CBC_SHA256": "DH-DSS-AES256-SHA256",
    "TLS_DH_RSA_WITH_AES_256_CBC_SHA256": "DH-RSA-AES256-SHA256",
    "TLS_DHE_DSS_WITH_AES_256_CBC_SHA256": "DHE-DSS-AES256-SHA256",
    "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256": "DHE-RSA-AES256-SHA256",
    "TLS_DH_anon_WITH_AES_128_CBC_SHA256": "ADH-AES128-SHA256",
    "TLS_DH_anon_WITH_AES_256_CBC_SHA256": "ADH-AES256-SHA256",
    "TLS_GOSTR341094_WITH_28147_CNT_IMIT": "GOST94-GOST89-GOST89",
    "TLS_GOSTR341001_WITH_28147_CNT_IMIT": "GOST2001-GOST89-GOST89",
    "TLS_GOSTR341001_WITH_NULL_GOSTR3411": "GOST94-NULL-GOST94",
    "TLS_GOSTR341094_WITH_NULL_GOSTR3411": "GOST2001-GOST89-GOST89",
    "TLS_RSA_WITH_CAMELLIA_256_CBC_SHA": "CAMELLIA256-SHA",
    "TLS_DH_DSS_WITH_CAMELLIA_256_CBC_SHA": "DH-DSS-CAMELLIA256-SHA",
    "TLS_DH_RSA_WITH_CAMELLIA_256_CBC_SHA": "DH-RSA-CAMELLIA256-SHA",
    "TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA": "DHE-DSS-CAMELLIA256-SHA",
    "TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA": "DHE-RSA-CAMELLIA256-SHA",
    "TLS_DH_anon_WITH_CAMELLIA_256_CBC_SHA": "ADH-CAMELLIA256-SHA",
    "TLS_PSK_WITH_RC4_128_SHA": "PSK-RC4-SHA",
    "TLS_PSK_WITH_3DES_EDE_CBC_SHA": "PSK-3DES-EDE-CBC-SHA",
    "TLS_PSK_WITH_AES_128_CBC_SHA": "PSK-AES128-CBC-SHA",
    "TLS_PSK_WITH_AES_256_CBC_SHA": "PSK-AES256-CBC-SHA",
    "TLS_RSA_WITH_SEED_CBC_SHA": "SEED-SHA",
    "TLS_DH_DSS_WITH_SEED_CBC_SHA": "DH-DSS-SEED-SHA",
    "TLS_DH_RSA_WITH_SEED_CBC_SHA": "DH-RSA-SEED-SHA",
    "TLS_DHE_DSS_WITH_SEED_CBC_SHA": "DHE-DSS-SEED-SHA",
    "TLS_DHE_RSA_WITH_SEED_CBC_SHA": "DHE-RSA-SEED-SHA",
    "TLS_DH_anon_WITH_SEED_CBC_SHA": "ADH-SEED-SHA",
    "TLS_RSA_WITH_AES_128_GCM_SHA256": "AES128-GCM-SHA256",
    "TLS_RSA_WITH_AES_256_GCM_SHA384": "AES256-GCM-SHA384",
    "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256": "DHE-RSA-AES128-GCM-SHA256",
    "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384": "DHE-RSA-AES256-GCM-SHA384",
    "TLS_DH_RSA_WITH_AES_128_GCM_SHA256": "DH-RSA-AES128-GCM-SHA256",
    "TLS_DH_RSA_WITH_AES_256_GCM_SHA384": "DH-RSA-AES256-GCM-SHA384",
    "TLS_DHE_DSS_WITH_AES_128_GCM_SHA256": "DHE-DSS-AES128-GCM-SHA256",
    "TLS_DHE_DSS_WITH_AES_256_GCM_SHA384": "DHE-DSS-AES256-GCM-SHA384",
    "TLS_DH_DSS_WITH_AES_128_GCM_SHA256": "DH-DSS-AES128-GCM-SHA256",
    "TLS_DH_DSS_WITH_AES_256_GCM_SHA384": "DH-DSS-AES256-GCM-SHA384",
    "TLS_DH_anon_WITH_AES_128_GCM_SHA256": "ADH-AES128-GCM-SHA256",
    "TLS_DH_anon_WITH_AES_256_GCM_SHA384": "ADH-AES256-GCM-SHA384",
    "TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256": "CAMELLIA128-SHA256",
    "TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA256": "DH-DSS-CAMELLIA128-SHA256",
    "TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA256": "DH-RSA-CAMELLIA128-SHA256",
    "TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256": "DHE-DSS-CAMELLIA128-SHA256",
    "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256": "DHE-RSA-CAMELLIA128-SHA256",
    "TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA256": "ADH-CAMELLIA128-SHA256",
    "SSL_CK_RC4_128_WITH_MD5": "RC4-MD5",
    "SSL_CK_RC4_128_EXPORT40_WITH_MD5": "EXP-RC4-MD5",
    "SSL_CK_RC2_128_CBC_WITH_MD5": "RC2-CBC-MD5",
    "SSL_CK_RC2_128_CBC_EXPORT40_WITH_MD5": "EXP-RC2-CBC-MD5",
    "SSL_CK_IDEA_128_CBC_WITH_MD5": "IDEA-CBC-MD5",
    "SSL_CK_DES_64_CBC_WITH_MD5": "DES-CBC-MD5",
    "SSL_CK_DES_64_CBC_WITH_SHA": "DES-CBC-SHA",
    "SSL_CK_DES_192_EDE3_CBC_WITH_MD5": "DES-CBC3-MD5",
    "SSL_CK_DES_192_EDE3_CBC_WITH_SHA": "DES-CBC3-SHA",
    "SSL_CK_RC4_64_WITH_MD5": "RC4-64-MD5",
    "SSL_CK_DES_64_CFB64_WITH_MD5_1": "DES-CFB-M1",

}
