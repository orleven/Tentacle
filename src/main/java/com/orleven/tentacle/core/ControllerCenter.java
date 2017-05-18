package com.orleven.tentacle.core;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.dao.imp.VulnerReportDaoImp;
import com.orleven.tentacle.dao.imp.VulnerScriptDaoImp;

/**
 * 控制中心类
 * @author orleven
 * @date 2017年5月13日
 */
@Component
public class ControllerCenter {
	
//	@Autowired
//	private VulnerScriptDaoImp vulnerScriptDaoImp;
	
	@Autowired
	private VulnerReportDaoImp vulnerReportDaoImp;
	
	public ControllerCenter(){
		
	}
	
	/**
	 * 初始化
	 * @data 2017年5月17日
	 */
	public void init(){
		
		// 连接数据库
		vulnerReportDaoImp.connectDB();
		if(!vulnerReportDaoImp.isTableExist()){
			vulnerReportDaoImp.createTable();
		}
//		vulnerScriptDaoImp.connectDB();
//		if(!vulnerScriptDaoImp.isTableExist()){
//			vulnerScriptDaoImp.createTable();
//		}
	}
	
	public void work(){
		
	}
}
