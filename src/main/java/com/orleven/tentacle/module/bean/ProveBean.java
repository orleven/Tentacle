package com.orleven.tentacle.module.bean;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.define.Message;

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
	
	public void addSendMessage(String sendMessage){
		this.sendMessage += sendMessage + Message.ContextPartingLine;
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
	
	public void addReceiveMessage(String receiveMessage){
		this.receiveMessage += receiveMessage + Message.ContextPartingLine;
	}
}
