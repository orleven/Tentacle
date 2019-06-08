# Tentacle

```
.___________. _______ .__   __. .___________.    ___       ______  __       _______
|           ||   ____||  \ |  | |           |   /   \     /      ||  |     |   ____| {1.0.0#stable}
`---|  |----`|  |__   |   \|  | `---|  |----`  /  ^  \   |  ,----'|  |     |  |__
    |  |     |   __|  |  . `  |     |  |      /  /_\  \  |  |     |  |     |   __|
    |  |     |  |____ |  |\   |     |  |     /  _____  \ |  `----.|  `----.|  |____
    |__|     |_______||__| \__|     |__|    /__/     \__\ \______||_______||_______| http://www.orleven.com


```

Tentacle is a POC vulnerability verification and exploit framework. It supports free extension of exploits and uses POC scripts. It supports calls to zoomeye, fofa, shodan and other APIs to perform bulk vulnerability verification for multiple targets. (Still in DEV...)

[![Python 3.6](https://img.shields.io/badge/python-3.6-yellow.svg)](https://www.python.org/)

![show](show/test.png)

### Install

```
pip3 install -r requestment.txt
```

### Usage

```
# Show help for tentacle.
python3 tentacle.py --help

# Show all modual, and you can see it in `script` path.
python3 tentacle.py --show

# Load modual by -m (e.g. script/info/web_status,@web)
python3 tentacle.py -m script/info/web_status               # Load web_status module
python3 tentacle.py -m @web                                 # Load all module of web path
python3 tentacle.py -m script/info/web_status,@web          # Load all module of web path and web_status module
python3 tentacle.py -m "*"                                    # Load all module of script path

# Load target by iS/iN/iF/iT/iX/iE/gg/sd/ze/ff.
# If you don't enter the target port, then it will try the default port number by server_type.
python3 tentacle.py -m script/info/web_status -iS www.examples.com             # Load target by url or host 
python3 tentacle.py -m script/info/web_status -iN 192.168.111.0/24             # Load target by network
python3 tentacle.py -m script/info/web_status -iF target.txt                   # Load target by file
python3 tentacle.py -m script/info/web_status -iT dcc54c3e1cc2c2e1             # Load target by recode's target
python3 tentacle.py -m script/info/web_status -iX nmap_xml.xml                 # Load target by nmap.xml
python3 tentacle.py -m script/info/web_status -iE "powered by discuz"          # Load target by baidu/bing/360so
python3 tentacle.py -m script/info/web_status -gg 'intext:powered by discuz'   # Load target by google api
python3 tentacle.py -m script/info/web_status -sd 'apache'                     # Load target by shodan api
python3 tentacle.py -m script/info/web_status -ze 'app:weblogic'               # Load target by zoomeye api
python3 tentacle.py -m script/info/web_status -ff 'domain="example.com"'       # Load target by fofa api
python3 tentacle.py -m script/info/web_status -fft                             # Load target by fofa today api

# Show all function of module by -f show or -f help
python3 tentacle.py -m script/info/web_status -f show
python3 tentacle.py -m script/info/web_status -f help

# Use function of modual by -m and -f  (e.g. -m web_status -f prove), and you should make sure the function of module is exist.
python3 tentacle.py -m script/info/web_status -f prove

# Show task's result by -tS 
python3 tentacle.py -tS 8d4b37597aaec25e

# Export task's result by -tS to test.xlsx
python3 tentacle.py -tS 8d4b37597aaec25e  -o test

# Update by git
python3 tentacle.py --update
```

### Update

* [2018-11-15] Code refactoring and fix bug.
* [2019-04-24] Fix bug and add script.
* [2019-06-08] Code refactoring and add port scan.

### Thanks

1. [Sqlmap](https://github.com/sqlmapproject/sqlmap)
2. [POC-T](https://github.com/Xyntax/POC-T)

