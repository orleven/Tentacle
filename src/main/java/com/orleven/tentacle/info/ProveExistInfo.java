package com.orleven.tentacle.info;

import java.util.ArrayList;
import java.util.Map;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * 证明漏洞存在的信息
 * @author orleven
 * @time  2016年12月15日
 */

@Component
@Scope("prototype")
public class ProveExistInfo {
	
	/**
	 * 漏洞是否存在：1 为存在；-1为不存在；0为验证失败或者未知。
	 */
	private int isVulnerable ;
	
	/**
	 * 漏洞验证标志
	 */
	private String proveFlag;
	
	/**
	 * 漏洞验证信息,返回数据
	 */
	private ArrayList<String> retDate;
	
	/**
	 * 漏洞验证信息，发送数据
	 */
	private ArrayList<String> sendDate;
	
	public ProveExistInfo(String proveFlag){
		this.isVulnerable = 0;
		this.proveFlag = proveFlag;
		this.sendDate = new ArrayList();
		this.retDate = new ArrayList();
	}
	
	public ProveExistInfo(){
		this.isVulnerable = 0;
		this.proveFlag = "id";
		this.sendDate = new ArrayList();
		this.retDate = new ArrayList();
	}
	
	public int getIsVulnerable() {
		return isVulnerable;
	}
	
	public void setIsVulnerable(int isVulnerable) {
		this.isVulnerable = isVulnerable;
	}
	
	public ArrayList<String>getRetDate() {
		return retDate;
	}

	public void setSendDate(ArrayList<String> sendDate) {
		this.sendDate = sendDate;
	}
	
	public ArrayList<String>getSendDate() {
		return sendDate;
	}

	public void setRetDate(ArrayList<String> retDate) {
		this.retDate = retDate;
	}
	
	public String getProveFlag() {
		return proveFlag;
	}

	public void setProveFlag(String proveFlag) {
		this.proveFlag = proveFlag;
	}
	
}
