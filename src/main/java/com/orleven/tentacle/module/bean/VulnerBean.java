package com.orleven.tentacle.module.bean;

import java.util.ArrayList;
import java.util.List;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.define.Permeate;
import com.orleven.tentacle.entity.VulnerScript;

/**
 * 漏洞bean类
 * @author orleven
 * @date 2017年3月17日
 */
@Component
@Scope("prototype")
public class VulnerBean{
	
	/**
	 * 漏洞验证数据
	 */
	private ProveBean proveBean;
//	private ProveBean proveBeans;
	
	
	/**
	 * 是否存在漏洞
	 */
	private int isVulner;
	
	private VulnerScript vulner;

	public VulnerBean() {
//		proveBeans = new ArrayList<ProveBean>();
		isVulner = Permeate.isNotVerified;
	}
	
	public VulnerBean(VulnerScript vulner) {
		this.vulner = vulner;
//		proveBeans = new ArrayList<ProveBean>();
		isVulner = Permeate.isNotVerified;
	}
	
//	public void setProveBeans(List<ProveBean> proveBeans){
//		this.proveBeans = proveBeans;
//	}
//	
//	public List<ProveBean> getProveBeans(){
//		return proveBeans;
//	}
	
	public void setProveBean(ProveBean proveBean){
		this.proveBean = proveBean;
	}
	
	public ProveBean getProveBeans(){
		return proveBean;
	}
	
	
	public void setIsVulner(int isVulner){
		this.isVulner = isVulner;
	}
	
	public int getIsVulner(){
		return isVulner;
	}
	
	public void setVulner(VulnerScript vulner){
		this.vulner = vulner;
	}
	
	public VulnerScript getVulner(){
		return vulner;
	}
}
