package com.orleven.tentacle.permeate.bean;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * 漏洞验证数据bean
 * @author orleven
 * @date 2017年3月18日
 */
@Component
@Scope("prototype")
public class ProveBean {
	
	/**
	 * 发送数据
	 */
	private String sendMessage;
	
	/**
	 * 接受数据
	 */
	private String receiveMessage;
	
	public void setSendMessage(String sendMessage){
		this.sendMessage = sendMessage;
	}
	
	public String getSendMessage(){
		return sendMessage;
	}
	
	public void setReceiveMessage(String receiveMessage){
		this.receiveMessage = receiveMessage;
	}
	public String getReceiveMessage(){
		return receiveMessage;
	}
}
