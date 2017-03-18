package com.orleven.tentacle.info;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * 针对某个漏洞的基础信息类
 * @author orleven
 * @time  2016年12月15日
 */
@Component
@Scope("prototype")
public class BaseServerInfo {
	
	/**
	 * ip 地址
	 */
	private String ip ;
	
	/**
	 * 端口
	 */
	private String port ;
	
	/**
	 * 域名，例如：www.baidu.com
	 */
	private String domainName;
	
	/**
	 * 服务名
	 */
	private String serviceName;
	
	/**
	 * 操作系统
	 */
	private String OS ;

	public void setip(String ip) {
		this.ip = ip;
	}
	
	public String getip() {
		return ip;
	}
	
	public void setPort(String port) {
		this.port = port;
	}
	
	public String getPort() {
		return port;
	}
	

	
	public void setServiceName(String serviceName) {
		this.serviceName = serviceName;
	}
	
	public String getServiceName() {
		return serviceName;
	}
	
	public void setDomainName(String domainName) {
		this.domainName = domainName;
	}
	
	public String getDomainName() {
		if(domainName==null){
			return getip();
		}
		return domainName;
	}
	
}
