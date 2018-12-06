# Tentacle

```
.___________. _______ .__   __. .___________.    ___       ______  __       _______
|           ||   ____||  \ |  | |           |   /   \     /      ||  |     |   ____|{0.1.7#test}
`---|  |----`|  |__   |   \|  | `---|  |----`  /  ^  \   |  ,----'|  |     |  |__
    |  |     |   __|  |  . `  |     |  |      /  /_\  \  |  |     |  |     |   __|
    |  |     |  |____ |  |\   |     |  |     /  _____  \ |  `----.|  `----.|  |____
    |__|     |_______||__| \__|     |__|    /__/     \__\ \______||_______||_______| http://www.orleven.com


```

Just for pentest.

[![Python 3.5](https://img.shields.io/badge/python-3.5-yellow.svg)](https://www.python.org/)

![show](https://raw.githubusercontent.com/orleven/Tentacle/master/show/test.png)

### Usage

```
# Show help for tentacle.
py -3 tentacle.py --help

# Show all modual, and you can see it in `script` path.
py -3 tentacle.py --show

# Load modual by -m (e.g. script/info/web_status,@web)
py -3 tentacle.py -m script/info/web_status               # Load web_status module
py -3 tentacle.py -m @web                                 # Load all module of web path
py -3 tentacle.py -m script/info/web_status,@web          # Load all module of web path and web_status module
py -3 tentacle.py -m *                                    # Load all module

# Load target by iS/iN/iF/iT/iX/iE/gg/sd/ze/ff.
py -3 tentacle.py -m script/info/web_status -iS www.examples.com             # Load target by url or host
py -3 tentacle.py -m script/info/web_status -iN 192.168.111.0/24             # Load target by network
py -3 tentacle.py -m script/info/web_status -iF target.txt                   # Load target by file
py -3 tentacle.py -m script/info/web_status -iT dcc54c3e1cc2c2e1             # Load target by recode's target
py -3 tentacle.py -m script/info/web_status -iX nmap_xml.txt                 # Load target by nmap.xml

py -3 tentacle.py -m script/info/web_status -iE "powered by discuz"          # Load target by baidu/bing/360so

py -3 tentacle.py -m script/info/web_status -gg 'intext:powered by discuz'   # Load target by google api
py -3 tentacle.py -m script/info/web_status -sd 'apache'                     # Load target by shodan api
py -3 tentacle.py -m script/info/web_status -ze 'app:weblogic'               # Load target by zoomeye api
py -3 tentacle.py -m script/info/web_status -ff 'domain="example.com"'         # Load target by fofa api

py -3 tentacle.py -m test -gh "163"     # Search github's infomation about pass,email by api(need adjust)

# Show all function of module by -f show or -f help
py -3 tentacle.py -m script/info/web_status -f show
py -3 tentacle.py -m script/info/web_status -f help

# Use function of modual by -m and -f  (e.g. -m web_status -f prove), and you should make sure the function of module is exist.
py -3 tentacle.py -m script/info/web_status -f prove

# Show task' result by -tS 
py -3 tentacle.py -tS 8d4b37597aaec25e

# Export task' result by -tS to test.xlsx
py -3 tentacle.py -tS 8d4b37597aaec25e  -o test

# Update by git
py -3 tentacle.py --update
```

### Update

* [2018-11-15] Code refactoring and fix  bug.
* [2018-11-22] fix log error bug.
* [2018-12-06] add config, e.g. proxy, api.

### Coming

1. struts2 mixtake bug
2. crawler module
3. module(script) clean up
4. server model
5. client model
6. port scan

### Thanks

1. Sqlmap
2. POC-T

