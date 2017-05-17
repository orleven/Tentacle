package com.orleven.tentacle.module.common;

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
	 * 加载字典
	 * @data 2017年5月16日
	 */
	public void load(String usernameDic,String passwordDic,String pathDic){
		if(usernameDic!=null&&!usernameDic.isEmpty()){
			this.usernames = FileUtil.readLines(usernameDic);
		}
		if(passwordDic!=null&&!passwordDic.isEmpty()){
			this.passwords = FileUtil.readLines(passwordDic);
		}
		if(pathDic!=null&&!pathDic.isEmpty()){
			this.paths = FileUtil.readLines(pathDic);
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
}
