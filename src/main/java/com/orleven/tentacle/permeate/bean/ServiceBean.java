package com.orleven.tentacle.permeate.bean;

import java.util.ArrayList;
import java.util.List;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * 服务bean
 * @author orleven
 * @date 2017年3月17日
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
	
	/**
	 * 基础信息
	 */
	private AssetInfoBean assetInfoBean;
	
	
	
	public ServiceBean(){
		
	}
	
	
	public ServiceBean(AssetInfoBean assetInfoBean){
		this.assetInfoBean = assetInfoBean;
	}
	
	public ServiceBean(AssetInfoBean assetInfoBean,String port){
		this.port = port;
		this.assetInfoBean = assetInfoBean;
	}
	
	public ServiceBean(AssetInfoBean assetInfoBean,String port,String serviceType){
		this.port = port;
		this.serviceType =serviceType;
		this.assetInfoBean = assetInfoBean;
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
	
	public AssetInfoBean getAssetInfoBean(){
		return assetInfoBean;
	}
	
	public void setAssetInfoBean(AssetInfoBean assetInfoBean){
		this.assetInfoBean = assetInfoBean;
	}
}
