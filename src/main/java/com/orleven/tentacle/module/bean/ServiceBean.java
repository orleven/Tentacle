package com.orleven.tentacle.module.bean;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * 服务bean
 * @author orleven
 * @date 2017年5月14日
 */
@Component
@Scope("prototype")
public class ServiceBean {
	/**
	 * 端口
	 */
	private String port;
	
	/**
	 * 服务类型,分为3389，22，21，web，redis等等
	 */
	private String serviceType;
	
	public ServiceBean(){}
	
	public ServiceBean(String port){
		this.port = port;
	}
	
	public ServiceBean(String port,String serviceType){
		this.port = port;
		this.serviceType = serviceType;
	}
	
	public void setPort(String port){
		this.port = port;
	}
	
	public void setServiceType(String serviceType){
		this.serviceType = serviceType;
	}

	
	public String getPort(){
		return port;
	}
	
	public String getServiceType(){
		return serviceType;
	}
}
