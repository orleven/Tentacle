
from lib.utils.connect import ClientSession
from script import Script, SERVICE_PORT_MAP

class POC(Script):

    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'thinkphp debug'
        self.keyword = ['thinkphp']
        self.info = 'thinkphp debug'
        self.type = 'info'
        self.level = 'info'
        self.refer = ''
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            pocs = ["is_not_exist"]
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            async with ClientSession() as session:
                for path in path_list:
                    for poc in pocs:
                        url = path + poc
                        async with session.get(url=url) as res:
                            if res != None:
                                text = await res.text()
                                if 'Environment Variables' in text:
                                    self.flag = 1
                                    self.res.append({"info": url, "key": "thinkphp debug"})
                                    break
