package com.orleven.tentacle.module.bean;

import java.util.List;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * SSH 服务bean，用来存放SSH信息的
 * @author orleven
 * @date 2017年3月17日
 */
@Component
@Scope("prototype")
public class SshServiceBean{
	
	/**
	 * 基本信息
	 */
	private BasicInfoBean basicInfoBean;
	
	/**
	 * 服务信息
	 */
	private ServiceBean serviceBean;


	public void setBasicInfoBean(BasicInfoBean basicInfoBean){
		this.basicInfoBean = basicInfoBean;
	}
	
	
	public BasicInfoBean getBasicInfoBean(){
		return basicInfoBean;
	}

	
	public void setServiceBean(ServiceBean serviceBean){
		this.serviceBean = serviceBean;
	}
	
	
	public ServiceBean getServiceBean(){
		return serviceBean;
	}
	

}
