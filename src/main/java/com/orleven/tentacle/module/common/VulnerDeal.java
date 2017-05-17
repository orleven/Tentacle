package com.orleven.tentacle.module.common;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Component;
import com.orleven.tentacle.entity.VulnerScript;
import com.orleven.tentacle.util.XMLUtil;


/**
 * 漏洞库处理（XML 漏洞库处理）
 * @author orleven
 * @date 2017年5月17日
 */
@Component  
public class VulnerDeal {

	/**
	 * 漏洞xml地址
	 */
	private String vulnerScriptPath  ;
	
	/**
	 * 所有检测项
	 */
	private List<VulnerScript> vulnerScripts;
	
	public VulnerDeal(){
		vulnerScripts = null;;
		vulnerScriptPath = "config/vulner.xml" ;
	}
	
	/**
	 * 加载所有漏洞脚本集合
	 * @data 2017年5月17日
	 * @param path
	 * @return
	 */
	public List<VulnerScript> loadVulnerScripts(){
		if(new File(vulnerScriptPath).exists()){
			vulnerScripts = new ArrayList<>();
			List<Map<String,String>> nodes = XMLUtil.listNodes(vulnerScriptPath);
	        if(nodes!=null){
	        	vulnerScripts = new ArrayList();
	        	for(Map<String,String> node:nodes){
	        		int vulnerId =  Integer.parseInt(node.get("vulnerId"));
	        		String vulnerName = node.get("vulnerName");
	        		String vulnerCVE = node.get("vulnerCVE");
	        		String vulnerDescribe = node.get("vulnerDescribe");
	        		String repaire = node.get("repaire");
	        		String vulnerType = node.get("vulnerType");
	        		String vulnerRank = node.get("vulnerRank");
	        		String scriptName = node.get("scriptName");
	        		String scriptType = node.get("scriptType");
	        		VulnerScript vulnerScript = new VulnerScript(vulnerId,vulnerName,vulnerCVE,vulnerDescribe,repaire,vulnerType,vulnerRank,scriptName,scriptType);
	        		vulnerScripts.add(vulnerScript);
	        	}
	        }
		} 
		return vulnerScripts;
	}

	public List<VulnerScript> getVulnerScript(){
		return vulnerScripts;
	}
    
	public String getVulnerScriptPath(){
		return vulnerScriptPath;
	}
	
	public void setVulnerScriptPath(String vulnerScriptPath){
		this.vulnerScriptPath =  vulnerScriptPath;
	}
}
