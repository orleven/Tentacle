package com.orleven.tentacle.permeate.bean;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * SSH 服务bean，用来存放SSH信息的
 * @author orleven
 * @date 2017年3月17日
 */
@Component
@Scope("prototype")
public class SshServiceBean extends ServiceBean{

	public SshServiceBean(){
		super();
	}
	
	/**
	 * 通过ServiceBean来设置参数值，即把它里面值都赋值掉
	 * @data 2017年3月18日
	 * @param serviceBean
	 */
	public SshServiceBean(ServiceBean serviceBean){
		super();
		setAssetInfoBean(serviceBean.getAssetInfoBean());
		setPort(serviceBean.getPort());
		setServiceType(serviceBean.getServiceType());
	}

	public void setValueByServiceBean(ServiceBean serviceBean){
		setAssetInfoBean(serviceBean.getAssetInfoBean());
		setPort(serviceBean.getPort());
		setServiceType(serviceBean.getServiceType());
	}
	
	

}
