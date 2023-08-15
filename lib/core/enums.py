#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

class CustomLogging:
    """日志等级"""

    SUCCESS = 9
    ERROR = 8
    WARNING = 7
    INFO = 6
    DEBUG = 5
    CRITICAL = 10

class EngineType:
    """
    引擎类型
    """

    BASE_ENGINE = "BaseEngine"
    VUL_ENGINE = "VulEngine"


class TaskStatus:
    """任务状态"""

    NONE = "None"
    INIT = "Init"
    RUN = "Run"
    STOP = "Stop"
    COMPLETE = "Complate"

class TargetStatus:
    INIT = "Init"
    PORTSCAN = "PortScan"
    FINGERPRINTSCAN = "FingerprintScan"
    VULSCAN = "VulScan"
    COMPLETE = "Complete"

class ScriptType:
    NONE = "None"
    PINGSCAN = "PingScan"
    FINGERPRINTSCAN = "FingerprintScan"
    VULSCAN = "VulScan"

class ServicePortMap:
    FTP = ('FTP', [21])
    SSH = ('SSH', [22])
    TELNET = ('TELNET', [23])
    SMTP = ('SMTP', [25])
    DNS = ('DNS', [53])
    GIILAB = ('GITLAB', [80, 443])
    COREMAIL = ('COREMAIL', [80, 443])
    WEB = ('WEB', [80, 81, 88, 443, 7001, 8000, 8001, 8080, 8081, 8090, 8443])
    HTTP = ('HTTP', [80, 81, 88, 7001, 8000, 8001, 8080, 8081])
    POP3 = ('POP3', [110])
    NETBIOS = ('NETBIOS', [139])
    LDAP = ('LDAP', [389])
    HTTPS = ('HTTPS', [443, 8443])
    VPN = ('VPN', [443, 4430])
    SMB = ('SMB', [445])
    RSYNC = ('RSYNC', [873])
    IMAP = ('IMAP', [993])
    JAVARMI = ('JAVARMI', [1099])
    SQLSERVER = ('SQLSERVER', [1433, 1434])
    ORACLE = ('ORACLE', [1521])
    ZOOKEEPER = ('ZOOKEEPER', [2181])
    DOCKER = ('DOCKER', [2375])
    GRAFANA = ('GRAFANA', [3000])
    MYSQL = ('MYSQL', [3306])
    RDP = ('RDP', [3389])
    POSTGRESQL = ('POSTGRESQL', [5432])
    VNC = ('VNC', [5900])
    REDIS = ('REDIS', [6379])
    WEBLOGIC = ('WEBLOGIC', [7001, 7002])
    TOMCAT = ('TOMCAT', [8080, 8081, 8443])
    AJP = ('AJP', [8009])
    CONFLUENCE = ('CONFLUENCE', [8080, 8090])
    ZABBIX = ('ZABBIX', [8069])
    ACTIVEMQ = ('ACTIVEMQ', [8161])
    SOLR = ('SOLR', [8983])
    SUPERVISOR = ('SUPERVISOR', [9001])
    WEBSPHERE = ('WEBSPHERE', [9080])
    ELASTICSEARCH = ('ELASTICSEARCH', [9200, 9300])
    MECACHE = ('MECACHE', [11211])
    RABBITMQ = ('RABBITMQ', [15672])
    DUBBO = ('DUBBO', [20880])
    MONGODB = ('MONGODB', [27017])
    PROXY = ('PROXY', [1080, 8080])
    UNKNOWN = ('UNKNOWN', [])

    TOP10 = (UNKNOWN[0], [21, 22, 80, 443, 3389, 6379, 7001, 8080, 8009, 8443])
    TOP50 = (UNKNOWN[0], [21, 22, 23, 25, 80, 81, 88, 109, 110, 161, 389, 443, 445, 465, 636, 873, 993, 995, 1025, 1080, 1433, 1521,
              2049, 2121, 2181, 2222, 2375, 3128, 3306, 3389, 5060, 5900, 5984, 6379, 7001, 8000, 8080, 8089, 8161,
              8443, 8649, 8888, 8983, 9080, 9090, 9200, 9300, 11211, 15672, 27017])
    TOP100 = (UNKNOWN[0], [21, 22, 23, 25, 80, 81, 88, 109, 110, 135, 137, 138, 139, 143, 161, 389, 443, 445, 465, 554, 587, 636,
               873, 990, 993, 995, 1025, 1080, 1158, 1433, 1434, 1521, 1723, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
               2019, 2049, 2100, 2121, 2181, 2222, 2375, 2381, 2601, 2604, 3000, 3128, 3260, 3306, 3389, 4100, 4200,
               4430, 5000, 5060, 5432, 5631, 5632, 5800, 5900, 5984, 6379, 7001, 7070, 8000, 8008, 8009, 8069, 8080,
               8088, 8089, 8161, 8443, 8480, 8649, 8888, 9000, 9001, 9080, 9090, 9100, 9200, 9300, 10000, 11211, 14000,
               15672, 27017, 28017, 50000, 50030, 50060, 50070, 50075, 55672])
    TOP150 = (UNKNOWN[0], [9, 13, 19, 21, 22, 23, 25, 37, 53, 79, 80, 81, 88, 106, 109, 110, 113, 119, 135, 137, 138, 139, 143, 161,
               179, 199, 389, 427, 443, 445, 465, 512, 513, 514, 543, 548, 554, 587, 631, 636, 646, 873, 990, 993, 995,
               1025, 1026, 1027, 1028, 1080, 1110, 1158, 1433, 1434, 1500, 1521, 1701, 1720, 1723, 1755, 1900, 2000,
               2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2049, 2082, 2083, 2100, 2121, 2181, 2222, 2375, 2381,
               2500, 2601, 2604, 2717, 3000, 3128, 3260, 3306, 3389, 3986, 4100, 4200, 4786, 4899, 5000, 5051, 5060,
               5190, 5357, 5432, 5631, 5632, 5666, 5800, 5900, 5984, 6000, 6082, 6379, 6646, 7001, 7070, 7778, 8000,
               8008, 8009, 8069, 8080, 8083, 8088, 8089, 8161, 8443, 8480, 8649, 8787, 8888, 9000, 9001, 9080, 9090,
               9100, 9160, 9200, 9300, 9999, 10000, 11211, 14000, 15672, 17027, 27017, 28017, 32768, 50000, 50030,
               50060, 50070, 50075, 55672, 60010])
    TOP1000 = (UNKNOWN[0], [1, 3, 6, 9, 13, 17, 19, 20, 21, 22, 23, 24, 25, 30, 32, 37, 42, 49, 53, 70, 79, 80, 81, 82, 83, 84, 88,
                89, 99, 106, 109, 110, 113, 119, 125, 135, 139, 143, 146, 161, 163, 179, 199, 211, 222, 254, 255, 259,
                264, 280, 301, 306, 311, 340, 366, 389, 406, 416, 425, 427, 443, 444, 458, 464, 481, 497, 500, 512, 513,
                514, 524, 541, 543, 544, 548, 554, 563, 587, 593, 616, 625, 631, 636, 646, 648, 666, 667, 683, 687, 691,
                700, 705, 711, 714, 720, 722, 726, 749, 765, 777, 783, 787, 800, 808, 843, 873, 880, 888, 898, 900, 901,
                902, 911, 981, 987, 990, 992, 995, 999, 1000, 1001, 1007, 1009, 1010, 1021, 1022, 1023, 1024, 1025,
                1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042,
                1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059,
                1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076,
                1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093,
                1094, 1095, 1096, 1097, 1098, 1099, 1102, 1104, 1105, 1106, 1107, 1110, 1111, 1112, 1113, 1117, 1119,
                1121, 1122, 1123, 1126, 1130, 1131, 1137, 1141, 1145, 1147, 1148, 1151, 1154, 1163, 1164, 1165, 1169,
                1174, 1183, 1185, 1186, 1192, 1198, 1201, 1213, 1216, 1217, 1233, 1236, 1244, 1247, 1259, 1271, 1277,
                1287, 1296, 1300, 1309, 1310, 1322, 1328, 1334, 1352, 1417, 1433, 1443, 1455, 1461, 1494, 1500, 1503,
                1521, 1524, 1533, 1556, 1580, 1583, 1594, 1600, 1641, 1658, 1666, 1687, 1700, 1717, 1718, 1719, 1720,
                1723, 1755, 1761, 1782, 1801, 1805, 1812, 1839, 1862, 1863, 1875, 1900, 1914, 1935, 1947, 1971, 1974,
                1984, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2013, 2020, 2021, 2030,
                2033, 2034, 2038, 2040, 2041, 2042, 2045, 2046, 2047, 2048, 2065, 2068, 2099, 2103, 2105, 2106, 2111,
                2119, 2121, 2126, 2135, 2144, 2160, 2170, 2179, 2190, 2196, 2200, 2222, 2251, 2260, 2288, 2301, 2323,
                2366, 2381, 2382, 2393, 2399, 2401, 2492, 2500, 2522, 2525, 2557, 2601, 2604, 2607, 2638, 2701, 2710,
                2717, 2725, 2800, 2809, 2811, 2869, 2875, 2909, 2920, 2967, 2998, 3000, 3003, 3005, 3006, 3011, 3013,
                3017, 3030, 3052, 3071, 3077, 3128, 3168, 3211, 3221, 3260, 3268, 3283, 3300, 3306, 3322, 3323, 3324,
                3333, 3351, 3367, 3369, 3370, 3371, 3389, 3404, 3476, 3493, 3517, 3527, 3546, 3551, 3580, 3659, 3689,
                3703, 3737, 3766, 3784, 3800, 3809, 3814, 3826, 3827, 3851, 3869, 3871, 3878, 3880, 3889, 3905, 3914,
                3918, 3920, 3945, 3971, 3986, 3995, 3998, 4000, 4001, 4002, 4003, 4004, 4005, 4045, 4111, 4125, 4129,
                4224, 4242, 4279, 4321, 4343, 4443, 4444, 4445, 4449, 4550, 4567, 4662, 4848, 4899, 4998, 5000, 5001,
                5002, 5003, 5009, 5030, 5033, 5050, 5054, 5060, 5080, 5087, 5100, 5101, 5120, 5190, 5200, 5214, 5221,
                5225, 5269, 5280, 5298, 5357, 5405, 5414, 5431, 5440, 5500, 5510, 5544, 5550, 5555, 5560, 5566, 5631,
                5633, 5666, 5678, 5718, 5730, 5800, 5801, 5810, 5815, 5822, 5825, 5850, 5859, 5862, 5877, 5900, 5901,
                5902, 5903, 5906, 5910, 5915, 5922, 5925, 5950, 5952, 5959, 5960, 5961, 5962, 5987, 5988, 5998, 5999,
                6000, 6001, 6002, 6003, 6004, 6005, 6006, 6009, 6025, 6059, 6100, 6106, 6112, 6123, 6129, 6156, 6346,
                6379, 6389, 6502, 6510, 6543, 6547, 6565, 6566, 6580, 6646, 6666, 6667, 6668, 6689, 6692, 6699, 6779,
                6788, 6792, 6839, 6881, 6901, 6969, 7000, 7001, 7004, 7007, 7019, 7025, 7070, 7100, 7103, 7106, 7200,
                7402, 7435, 7443, 7496, 7512, 7625, 7627, 7676, 7741, 7777, 7800, 7911, 7920, 7937, 7999, 8000, 8001,
                8007, 8008, 8009, 8010, 8021, 8031, 8042, 8045, 8080, 8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088,
                8089, 8093, 8099, 8180, 8192, 8193, 8200, 8222, 8254, 8290, 8291, 8300, 8333, 8383, 8400, 8402, 8443,
                8500, 8600, 8649, 8651, 8654, 8701, 8800, 8873, 8888, 8899, 8994, 9000, 9001, 9002, 9009, 9010, 9040,
                9050, 9071, 9080, 9090, 9099, 9100, 9101, 9102, 9110, 9200, 9207, 9220, 9290, 9415, 9418, 9485, 9500,
                9502, 9535, 9575, 9593, 9594, 9618, 9666, 9876, 9877, 9898, 9900, 9917, 9929, 9943, 9968, 9998, 9999,
                10000, 10001, 10002, 10003, 10009, 10012, 10024, 10082, 10180, 10215, 10243, 10566, 10616, 10621, 10626,
                10628, 10778, 11110, 11967, 12000, 12174, 12265, 12345, 13456, 13722, 13782, 14000, 14238, 14441, 15000,
                15002, 15003, 15660, 15742, 16000, 16012, 16016, 16018, 16080, 16113, 16992, 17877, 17988, 18040, 18101,
                18988, 19101, 19283, 19315, 19350, 19780, 19801, 19842, 20000, 20005, 20031, 20221, 20828, 21571, 22939,
                23502, 24444, 24800, 25734, 26214, 27000, 27352, 27355, 27715, 28201, 30000, 30718, 30951, 31038, 31337,
                32768, 32769, 32770, 32771, 32772, 32773, 32774, 32775, 32776, 32777, 32778, 32779, 32780, 32781, 32782,
                32783, 32784, 33354, 33899, 34571, 34572, 35500, 38292, 40193, 40911, 41511, 42510, 44176, 44442, 44501,
                45100, 48080, 49152, 49153, 49154, 49155, 49156, 49157, 49158, 49159, 49160, 49163, 49165, 49167, 49175,
                49400, 49999, 50000, 50001, 50002, 50006, 50300, 50389, 50500, 50636, 50800, 51103, 51493, 52673, 52822,
                52848, 52869, 54045, 54328, 55055, 55555, 55600, 56737, 57294, 57797, 58080, 60020, 60443, 61532, 61900,
                62078, 63331, 64623, 64680, 65000, 65129, 65389])
    ALL = (UNKNOWN[0], [x for x in range(1, 65536)])

    # 未使用
    WEB_LIST = (WEB[0], [x for x in [
        COREMAIL, WEB, HTTP, HTTPS, VPN, DOCKER, WEBLOGIC, TOMCAT, CONFLUENCE, ZABBIX, ACTIVEMQ, GRAFANA, GIILAB,
        SUPERVISOR, WEBSPHERE, ELASTICSEARCH, RABBITMQ, SOLR, UNKNOWN, PROXY]
    ])
    NOT_WEB_LIST = (UNKNOWN[0], [x for x in [
        FTP, SSH, TELNET, SMTP, DNS, POP3, NETBIOS, LDAP, SMB, RSYNC, IMAP, JAVARMI, SQLSERVER, ORACLE, ZOOKEEPER,
        DOCKER, MYSQL, RDP, POSTGRESQL, VNC, REDIS, MECACHE, DUBBO, MONGODB, UNKNOWN, PROXY]
    ])