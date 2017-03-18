package com.orleven.tentacle.permeate.bean;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * 资产基础信息bean
 * @author orleven
 * @date 2017年3月18日
 */
@Component
@Scope("prototype")
public class AssetInfoBean {

	/**
	 * host ，即ip
	 */
	private String host;
	
	/**
	 * domain ，即域名
	 */
	private String domain;
	
	/**
	 * 操作系统
	 */
	private String OS;
	
	public AssetInfoBean(){
	
	}
	
	public void setOS(String OS) {
		this.OS = OS;
	}
	
	public String getOS() {
		return OS;
	}
	
	public AssetInfoBean(String host){
		this.host = host;
	}
	
	public AssetInfoBean(String host,String domain){
		this.domain = domain;
		this.host = host;
	}
	
	public AssetInfoBean(String host,String domain,String OS){
		this.host = host;
		this.domain = domain; 
		this.OS = OS;
	}
	

	
	public void setHost(String host){
		this.host = host;
	}
	
	
	public String getDomain(){
		return domain;
	}
	
	public void setDomain(String domain){
		this.domain = domain;
	}
	
	
	public String getHost(){
		return host;
	}
}
