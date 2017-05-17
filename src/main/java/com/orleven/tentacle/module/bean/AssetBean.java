package com.orleven.tentacle.module.bean;

import java.util.ArrayList;
import java.util.List;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;
/**
 * 资产 bean，即单个ip
 * @author orleven
 * @date 2017年5月14日
 */
@Component
@Scope("prototype")
public class AssetBean {
	
	/**
	 * 基本信息
	 */
	private BasicInfoBean basicInfoBean;
	/**
	 * 服务集合
	 */
	private List<ServiceBean> serviceBeans;
	
	public AssetBean(){
		serviceBeans = new ArrayList();
	}
	
	public void setBasicInfoBean(BasicInfoBean basicInfoBean){
		this.basicInfoBean = basicInfoBean;
	}
	
	
	public BasicInfoBean getBasicInfoBean(){
		return basicInfoBean;
	}

	
	public void setServiceBeans(List<ServiceBean> serviceBeans){
		this.serviceBeans = serviceBeans;
	}
	
	
	public List<ServiceBean> getServiceBeans(){
		return serviceBeans;
	}
	
	/**
	 * 根据端口添加ServiceBean
	 * @data 2017年5月15日
	 * @param ports
	 */
	public void setServiceBeans(String[] ports){
		for (String port : ports) {
			ServiceBean serviceBean = new ServiceBean(port);
			this.serviceBeans.add(serviceBean);
		}
	}
}
