package com.orleven.tentacle.info;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.http.message.BasicNameValuePair;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * 针对HTTP的漏洞的基础信息类
 * @author orleven
 * @time  2016年12月15日
 */
@Component
@Scope("prototype")
public class HTTPServerInfo extends BaseServerInfo{
	
	/**
	 * web 路径
	 */
	private String urlPath;
	
	/**
	 * 请求头
	 */
	private Map<String, String> httpHeaders;
	
	/**
	 * get请求参数
	 */
	private String getParameters;
	
	/**
	 * post 请求参数
	 */
	private List<BasicNameValuePair> postParameters;
	
	public HTTPServerInfo(String ip,String port){
		setServiceName("http");
		setip(ip);
		setPort(port);
		setHttpHeaders(new HashMap<String, String>());
	}
	
	public HTTPServerInfo(String domainName,String port,String ip){
		setServiceName("http");
		setip(ip);
		setPort(port);
		setDomainName(domainName);
		setHttpHeaders(new HashMap<String, String>());
	}
	
	public HTTPServerInfo(String domainName,String port,String urlPath,String ip){
		setServiceName("http");
		setip(ip);
		setPort(port);
		this.urlPath = urlPath;
		setDomainName(domainName);
		setHttpHeaders(new HashMap<String, String>());
	}
	
	
	public HTTPServerInfo(){
		setServiceName("http");
	}
	

	public void setUrlPath(String urlPath) {
		this.urlPath = urlPath;
	}
	
	public String getUrlPath() {
		return urlPath;
	}
	
	public void setGetParameters(String getParameters) {
		this.getParameters = getParameters;
	}
	
	public String  getGetParameters() {
		return getParameters;
	}
	
	public void setPostParameters(List<BasicNameValuePair> postParameters) {
		this.postParameters = postParameters;
	}
	
	public List<BasicNameValuePair>  getPostParameters() {
		return postParameters;
	}

	public Map<String,String> getHttpHeaders(){
		return httpHeaders;
	}
	
	public void setHttpHeaders(Map<String,String> httpHeaders){
		this.httpHeaders = httpHeaders;
	}
	
	public String getTargetUrl(){
		String targetUrl = getServiceName()+"://";
		if(getDomainName().length()>0){
			targetUrl += getDomainName();
		}else{
			targetUrl += getip();
		}
		if(getPort().length()<=0){
			targetUrl+=":80";
		}else{
			targetUrl += ":" + getPort();
		}
		if(urlPath!=null){
			targetUrl += urlPath;
		}
		if(getParameters!=null){
			targetUrl += "?" + getParameters;
		}
		return targetUrl;
	}
	
}
