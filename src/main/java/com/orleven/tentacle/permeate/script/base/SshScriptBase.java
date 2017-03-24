package com.orleven.tentacle.permeate.script.base;

import java.util.HashMap;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.permeate.bean.SshServiceBean;
import com.orleven.tentacle.permeate.bean.WebServiceBean;


/**
 * SSH 服务
 * @author orleven
 * @date 2017年3月22日
 */
@Component
@Scope("prototype")
public abstract class SshScriptBase  extends AbstractScriptBase{
	/**
	 * 检测对象
	 */
	private SshServiceBean sshServiceBean;
	
	private String username;
	
	private String password;
	
	public SshScriptBase(){
		super();
	}
	
	public void setSshServiceBean(SshServiceBean sshServiceBean) {
		this.sshServiceBean = sshServiceBean;
	}
	
	public SshServiceBean getSshServiceBean() {
		return sshServiceBean;
	}
	
	public void setUsername(String username) {
		this.username = username;
	}
	
	public String getUsername() {
		return username;
	}
	
	public void setSshPassword(String password) {
		this.password = password;
	}
	
	public String getSshPassword() {
		return password;
	}
	
	/**
	 * 验证
	 * @data 2017年3月24日
	 */
	public void prove() {
		
	}
	
	/**
	 * 命令执行
	 * @data 2017年3月18日
	 * @param command
	 */
	public void execCommand(String command) {
		
	}
	

	/**
	 * 文件上传
	 * @data 2017年3月23日
	 * @param inFile 本地文件
	 * @param outFile 上传地址
	 */
	public void uploadFile(String inFile,String outFile) {
		
	}
}
