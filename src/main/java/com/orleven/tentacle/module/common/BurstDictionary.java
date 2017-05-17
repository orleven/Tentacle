package com.orleven.tentacle.module.common;

import java.io.File;
import java.util.List;

import org.springframework.stereotype.Component;
import com.orleven.tentacle.util.FileUtil;

/**
 * 字典
 * @author orleven
 * @date 2017年5月16日
 */
@Component  
public class BurstDictionary {
	
	/**
	 * 用户名
	 */
	private List<String> usernames = null;
	
	/**
	 * 密码
	 */
	private List<String> passwords = null;
	
	/**
	 * 网站目录
	 */
	private List<String> paths = null;
	
	/**
	 * 用户字典地址
	 */
	private String usernameDicPath = null;
	
	/**
	 * 密码字典地址
	 */
	private String passwordDicPath = null;
	
	/**
	 * 网站地址字典地址
	 */
	private String pathDicPath = null;
	
	public BurstDictionary(){
		this.usernameDicPath = "config/username.txt";
		this.passwordDicPath = "config/password.txt";
		this.pathDicPath = "config/path.txt";
	}
	/**
	 * 加载字典
	 * @data 2017年5月16日
	 */
	public void load(){
		if(new File(usernameDicPath).exists()){
			this.usernames = FileUtil.readLines(usernameDicPath);
		}
		if(new File(passwordDicPath).exists()){
			this.passwords = FileUtil.readLines(passwordDicPath);
		}
		if(new File(pathDicPath).exists()){
			this.paths = FileUtil.readLines(pathDicPath);
		} 
	}
	
	public List<String> getUsernames(){
		return usernames;
	}
	
	public List<String> getPasswords(){
		return passwords;
	}
	
	public List<String> getPaths(){
		return paths;
	}
	
	public String getUsernameDicPath(){
		return usernameDicPath;
	}
	
	public void setUsernameDicPath(String usernameDicPath){
		this.usernameDicPath =  usernameDicPath;
	}
	
	public String getPasswordDicPath(){
		return passwordDicPath;
	}
	
	public void setPasswordDicPath(String passwordDicPath){
		this.passwordDicPath =  passwordDicPath;
	}
	
	public String getPathDicPath(){
		return pathDicPath;
	}
	
	public void setPathDicPath(String pathDicPath){
		this.pathDicPath =  pathDicPath;
	}
}
