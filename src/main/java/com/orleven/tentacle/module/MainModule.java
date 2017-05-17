package com.orleven.tentacle.module;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import com.orleven.tentacle.config.ConfigDBConfig;
import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.dao.imp.VulnerScriptDaoImp;
import com.orleven.tentacle.define.Permeate;
import com.orleven.tentacle.entity.VulnerScript;
import com.orleven.tentacle.module.bean.AssetBean;
import com.orleven.tentacle.module.bean.BasicInfoBean;
import com.orleven.tentacle.module.bean.ServiceBean;
import com.orleven.tentacle.module.bean.SshServiceBean;
import com.orleven.tentacle.module.bean.WebServiceBean;
import com.orleven.tentacle.module.pentest.SshAbstractScript;
import com.orleven.tentacle.module.pentest.WebAbstractScript;

@Component
public class MainModule {
	
	@Autowired
	private ConfigDBConfig  configDBconfig;
	
	@Autowired
	private VulnerScriptDaoImp vulnerDaoImp;
	
	public void init(){
		// 数据库初始化
//		configDBconfig = IOC.ctx.getBean(ConfigDBConfig.class);
//		configDBconfig.setConfigDataSource(new DBConfig().configDataSource());

		try {
			configDBconfig.connectConfigDB();
			vulnerDaoImp.setConfigConnection(configDBconfig.getConfigConnection());
		} catch (Exception e) {
			e.printStackTrace();
		}	
		
	}
	
	


}
