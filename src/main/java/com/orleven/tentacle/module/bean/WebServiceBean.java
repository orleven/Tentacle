package com.orleven.tentacle.module.bean;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * Web 服务bean，用来存放web信息的
 * @author orleven
 * @date 2017年3月17日
 */
@Component
@Scope("prototype")
public class WebServiceBean{

	/**
	 * 基本信息
	 */
	private BasicInfoBean basicInfoBean;
	
	/**
	 * 服务信息
	 */
	private ServiceBean serviceBean;
	
	/**
	 * 协议类型
	 */
	private String protocolType;
	
	public WebServiceBean(){
		protocolType = "http";
	}
	
	public WebServiceBean(String protocolType){
		this.protocolType = protocolType;
	}
	
	
	public void setProtocolType(String protocolType){
		this.protocolType = protocolType;
	}

	public String getProtocolType(){
		return protocolType;
	}
	
	public void setBasicInfoBean(BasicInfoBean basicInfoBean){
		this.basicInfoBean = basicInfoBean;
	}
	
	
	public BasicInfoBean getBasicInfoBean(){
		return basicInfoBean;
	}

	
	public void setServiceBean(ServiceBean serviceBean){
		this.serviceBean = serviceBean;
	}
	
	
	public ServiceBean getServiceBeans(){
		return serviceBean;
	}
}
