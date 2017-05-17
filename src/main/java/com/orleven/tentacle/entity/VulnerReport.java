package com.orleven.tentacle.entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

/**
 * VulnerReport 主要收集资产的漏洞
 * @author orleven
 * @date 2017年5月16日
 */
@Entity
@Table(name="VulnerReport")
public class VulnerReport {
	
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ReportId") 
	private int reportId;
    
    
    /**
     * 漏洞主机
     */
    @Column(name = "Host") 
    private String host;
    
    /**
     * 漏洞端口
     */
    @Column(name = "Port") 
    private String port;
    
    /**
     * 端口类型
     */
    @Column(name = "Type") 
    private String type;
    
    /**
     * 索引，便于根进行查找，index的机制： 数字型ip数字型ip数字型ip数字型ip...
     */
    @Column(name = "Index") 
    private String index;
    
    /**
     * 对应的脚本id
     */
    @Column(name = "VulnerId") 
    private int vulnerId;
    
	/**
	 * 发送数据
	 */
    @Column(name = "SendMessage") 
	private String sendMessage;
	
	/**
	 * 接受数据
	 */
    @Column(name = "ReceiveMessage") 
	private String receiveMessage;
    
    /**
     * 漏洞时间
     */
    @Column(name = "Time") 
    private String time;
	
	public VulnerReport(int reportId,String host,String port,String type,String index,int vulnerId,String sendMessage,String receiveMessage,String time){
		this.reportId = reportId;
		this.host = host;
		this.port = port;
		this.type = type;
		this.index = index;
		this.vulnerId = vulnerId;
		this.sendMessage = sendMessage;
		this.receiveMessage = receiveMessage;
		this.time = time;
	}
	
	public VulnerReport(String host,String port,String type,String index,int vulnerId,String sendMessage,String receiveMessage,String time){
		this.host = host;
		this.port = port;
		this.type = type;
		this.index = index;
		this.vulnerId = vulnerId;
		this.sendMessage = sendMessage;
		this.receiveMessage = receiveMessage;
		this.time = time;
	}
    
	public int getReportId(){
		return reportId;
	}
	
	public void setReportId(int reportId){
		this.reportId =  reportId;
	}
	
	public String getHost(){
		return host;
	}
	
	public void setHost(String host){
		this.host =  host;
	}	
	
	public String getPort(){
		return port;
	}
	
	public void setPort(String port){
		this.port =  port;
	}	
	
	public String getType(){
		return type;
	}
	
	public void setType(String type){
		this.type =  type;
	}	
	
	public String getIndex(){
		return index;
	}
	
	public void setIndex(String index){
		this.index =  index;
	}	
	
	public int getVulnerId(){
		return vulnerId;
	}
	
	public void setVulnerId(int vulnerId){
		this.vulnerId =  vulnerId;
	}
	
	public String getSendMessage(){
		return sendMessage;
	}
	
	public void setSendMessage(String sendMessage){
		this.sendMessage =  sendMessage;
	}	
	
	public String getReceiveMessage(){
		return receiveMessage;
	}
	
	public void setReceiveMessage(String receiveMessage){
		this.receiveMessage =  receiveMessage;
	}	
	
	public String getTime(){
		return time;
	}
	
	public void setTime(String time){
		this.time =  time;
	}	
}
