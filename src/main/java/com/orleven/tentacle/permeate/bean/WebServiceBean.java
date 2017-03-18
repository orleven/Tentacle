package com.orleven.tentacle.permeate.bean;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * Web 服务bean，用来存放web信息的
 * @author orleven
 * @date 2017年3月17日
 */
@Component
@Scope("prototype")
public class WebServiceBean extends ServiceBean{

	/**
	 * 协议类型
	 */
	private String protocolType;
	
	public WebServiceBean(){
		super();
		protocolType = "http";
	}
	
	public WebServiceBean(String protocolType){
		super();
		this.protocolType = protocolType;
	}
	
	/**
	 * 通过ServiceBean来设置参数值，即把它里面值都赋值掉
	 * @data 2017年3月18日
	 * @param serviceBean
	 */
	public void setValueByServiceBean(ServiceBean serviceBean){
		setAssetInfoBean(serviceBean.getAssetInfoBean());
		setPort(serviceBean.getPort());
		setServiceType(serviceBean.getServiceType());
	}
	
	
	public WebServiceBean(ServiceBean serviceBean){
		super();
		setAssetInfoBean(serviceBean.getAssetInfoBean());
		setPort(serviceBean.getPort());
		setServiceType(serviceBean.getServiceType());
	}
	
	public void setProtocolType(String protocolType){
		this.protocolType = protocolType;
	}

	public String getProtocolType(){
		return protocolType;
	}
	
}
