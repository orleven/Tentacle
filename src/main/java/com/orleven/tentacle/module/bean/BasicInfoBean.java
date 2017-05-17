package com.orleven.tentacle.module.bean;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * 基础信息
 * @author orleven
 * @date 2017年5月15日
 */
@Component
@Scope("prototype")
public class BasicInfoBean {
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
	

	
	public void setOS(String OS) {
		this.OS = OS;
	}
	
	public String getOS() {
		return OS;
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
