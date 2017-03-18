package com.orleven.tentacle.permeate.bean;

import java.util.ArrayList;
import java.util.List;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.entity.Vulner;

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
	private List<ProveBean> proveBeans;
	
	
	/**
	 * 是否存在漏洞
	 */
	private int isVulner;
	
	private Vulner vulner;

	public VulnerBean() {
		proveBeans = new ArrayList<ProveBean>();
	}
	
	public VulnerBean(Vulner vulner) {
		this.vulner = vulner;
		proveBeans = new ArrayList<ProveBean>();
	}
	
	public void setProveBean(List<ProveBean> proveBeans){
		this.proveBeans = proveBeans;
	}
	
	public List<ProveBean> getProveBean(){
		return proveBeans;
	}
	
	public void setIsVulner(int isVulner){
		this.isVulner = isVulner;
	}
	
	public int getIsVulner(){
		return isVulner;
	}
	
	public void setVulner(Vulner vulner){
		this.vulner = vulner;
	}
	
	public Vulner getVulner(){
		return vulner;
	}
}
