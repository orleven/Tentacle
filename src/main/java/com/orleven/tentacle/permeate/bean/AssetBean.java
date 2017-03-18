package com.orleven.tentacle.permeate.bean;

import java.util.ArrayList;
import java.util.List;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * 资产bean，即单个ip
 * @author orleven
 * @date 2017年3月8日
 */
@Component
@Scope("prototype")
public class AssetBean {
	
	/**
	 * 资产基础信息
	 */
	private AssetInfoBean assetInfoBean ;
	
	/**
	 * 服务集合
	 */
	private List<ServiceBean> serviceBeans;
	

	public AssetBean(){
		serviceBeans = new ArrayList();
	}
	
	public AssetBean(AssetInfoBean assetInfoBean){
		this.assetInfoBean = assetInfoBean;
		this.serviceBeans = new ArrayList();
	}
	

	public AssetBean(AssetInfoBean assetInfoBean,String[] ports){
		this.assetInfoBean = assetInfoBean; 
		this.serviceBeans = new ArrayList();
	    for (String port : ports) {
	    	serviceBeans.add(new ServiceBean(assetInfoBean,port));
	    }
	}
	
	public void setAssetInfoBean(AssetInfoBean assetInfoBean){
		this.assetInfoBean = assetInfoBean;
	}
	
	public AssetInfoBean getAssetInfoBean(){
		return assetInfoBean;
	}

	
	public void setServiceBeans(List<ServiceBean> serviceBeans){
		this.serviceBeans = serviceBeans;
	}
	
	
	public List<ServiceBean> getServiceBeans(){
		return serviceBeans;
	}
	
	
	public void setPorts(String[] ports){
	    for (String port : ports) {
	    	serviceBeans.add(new ServiceBean(assetInfoBean,port));
	    }
	}

}
