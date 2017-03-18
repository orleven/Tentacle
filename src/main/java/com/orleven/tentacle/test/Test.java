package com.orleven.tentacle.test;

import java.util.List;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.entity.Vulner;
import com.orleven.tentacle.permeate.bean.AssetBean;
import com.orleven.tentacle.permeate.bean.AssetInfoBean;
import com.orleven.tentacle.permeate.bean.ServiceBean;
import com.orleven.tentacle.permeate.bean.VulnerBean;
import com.orleven.tentacle.permeate.bean.WebServiceBean;
import com.orleven.tentacle.permeate.script.Struts2RCE045;

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
		String host = "192.168.111.148";
		String[] ports = {"9003","9002"};
		
		AssetInfoBean assetInfoBean = IOC.instance().getClassobj(AssetInfoBean.class);
		assetInfoBean.setHost(host);
		
		AssetBean assetBean = IOC.instance().getClassobj(AssetBean.class);
		assetBean.setAssetInfoBean(assetInfoBean);
		for (String port : ports) {
			ServiceBean serviceBean =new ServiceBean(assetInfoBean,port);
			assetBean.getServiceBeans().add(serviceBean);
		}
//		assetBean.setPorts(ports);
		System.out.println(1);
		Vulner vulner= new Vulner(0,"Struts2-045","","", "Remote Code Execute","Hign","Struts2RCE045");
	    for (ServiceBean serviceBean : assetBean.getServiceBeans()) {
	    	System.out.println(2);
	    	WebServiceBean webServiceBean = IOC.instance().getClassobj(WebServiceBean.class);
	    	webServiceBean.setValueByServiceBean(serviceBean);
	    	webServiceBean.setProtocolType("http");
	    	
	    	Struts2RCE045 struts2RCE045 = IOC.instance().getClassobj(Struts2RCE045.class);
	    	struts2RCE045.setWebServiceBean(webServiceBean);
	    	struts2RCE045.setAssetInfoBean(assetInfoBean);
	    	struts2RCE045.getVulnerBean().setVulner(vulner);
	    	struts2RCE045.setCookies("");
	    	struts2RCE045.prove();
	    	struts2RCE045.getVulnerBean();
	    	System.out.println(3);
	    }
	    System.out.println(5);
	}

}
