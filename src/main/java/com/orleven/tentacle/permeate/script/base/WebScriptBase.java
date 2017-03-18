package com.orleven.tentacle.permeate.script.base;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.http.message.BasicNameValuePair;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.permeate.bean.WebServiceBean;



/**
 * web漏洞利用虚拟基础类
 * @author orleven
 * @time  2016年12月20日
 */
@Component
@Scope("prototype")
public abstract class WebScriptBase  extends AbstractScriptBase{
	
	/**
	 * 检测对象
	 */
	private WebServiceBean webServiceBean;
	
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
	

	
	/**
	 * method 请求方法
	 */
	private String method;
	
	public WebScriptBase(){
		super();
		httpHeaders = new HashMap<String, String>();
		httpHeaders.put("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0");
		httpHeaders.put("Accept", "*/*");
		httpHeaders.put("Accept-Encoding", "gzip, deflate");
		httpHeaders.put("Content-Type","application/x-www-form-urlencoded");
	}
	
	/**
	 * 设置cookies
	 * @data 2017年3月18日
	 * @param cookies
	 */
	public void setCookies(String cookies){
		httpHeaders.put("Cookie", cookies);
	}

	public void setWebServiceBean(WebServiceBean webServiceBean) {
		this.webServiceBean = webServiceBean;
	}
	
	public WebServiceBean WebServiceBean() {
		return webServiceBean;
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
		if(webServiceBean.getProtocolType()==null)
			webServiceBean.setProtocolType("http");
		String targetUrl = webServiceBean.getProtocolType()+"://";
		if(getAssetInfoBean().getDomain()!=null&&getAssetInfoBean().getDomain().length()>0){
			targetUrl += getAssetInfoBean().getDomain();
		}else{
			targetUrl += getAssetInfoBean().getHost();
		}
		if(webServiceBean.getPort().length()<=0){
			targetUrl+=":80";
		}else{
			targetUrl += ":" + webServiceBean.getPort();
		}
		if(urlPath!=null){
			targetUrl += urlPath;
		}
		if(getParameters!=null){
			targetUrl += "?" + getParameters;
		}
		return targetUrl;
	}

	/**
	 * 命令执行
	 * @data 2017年3月18日
	 * @param command
	 */
	public void execCommand(String command) {
		
	}
	
	/**
	 * 漏洞验证
	 * @data 2017年3月18日
	 */
	public void prove() {
		
	}
}
