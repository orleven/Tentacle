package com.orleven.tentacle.entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

/**
 * 漏洞库
 * @author orleven
 * @date 2017年3月8日
 */
@Entity
@Table(name="VulnerScript")
public class VulnerScript {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "VulnerId") 
	private int vulnerId;
    
    /**
     * 漏洞名
     */
    @Column(name = "VulnerName") 
	private String vulnerName;
    
    /**
     * 漏洞CVE编号
     */
    @Column(name = "VulnerCVE") 
	private String vulnerCVE;
    
    /**
     * 漏洞描述
     */
    @Column(name = "VulnerDescribe") 
	private String vulnerDescribe;
    
    /**
     * 漏洞修补方式
     */
    @Column(name = "Repaire") 
	private String repaire;
    
    /**
     * 漏洞类型
     */
    @Column(name = "VulnerType") 
	private String vulnerType;
    
    /**
     * 漏洞风险等级
     */
    @Column(name = "VulnerRank") 
	private String vulnerRank;   
    
    /**
     * 对应执行脚本类名
     */
    @Column(name = "ScriptName") 
	private String scriptName;   
    
    /**
     * 对应执行脚本类型
     */
    @Column(name = "ScriptType") 
	private String scriptType;   
    
    public VulnerScript(){
	}
    
	public VulnerScript(int vulnerId,String vulnerName,String vulnerCVE,String vulnerDescribe,String repaire,String vulnerType,String vulnerRank,String scriptName,String scriptType){
		this.vulnerId = vulnerId;
		this.vulnerName = vulnerName;
		this.vulnerDescribe = vulnerDescribe;
		this.repaire = repaire;
		this.vulnerType = vulnerType;
		this.vulnerRank = vulnerRank;
		this.scriptName = scriptName;
		this.vulnerCVE = vulnerCVE;
		this.scriptType = scriptType;
	}
	
	public int getVulnerId(){
		return vulnerId;
	}
	
	public void setVulnerId(int vulnerId){
		this.vulnerId =  vulnerId;
	}
	
	public String getVulnerName(){
		return vulnerName;
	}
	
	public void setVulnerName(String vulnerName){
		this.vulnerName =  vulnerName;
	}	
    
	public String getVulnerCVE(){
		return vulnerCVE;
	}
	
	public void setVulnerCVE(String vulnerCVE){
		this.vulnerCVE =  vulnerCVE;
	}	
	
	public String getVulnerDescribe(){
		return vulnerDescribe;
	}
	
	public void setVulnerDescribe(String vulnerDescribe){
		this.vulnerDescribe =  vulnerDescribe;
	}	
	
	public String getRepaire(){
		return repaire;
	}
	
	public void setRepaire(String repaire){
		this.repaire =  repaire;
	}	
	
	public String getVulnerType(){
		return vulnerType;
	}
	
	public void setVulnerType(String vulnerType){
		this.vulnerType =  vulnerType;
	}	
	
	public String getVulnerRank(){
		return vulnerRank;
	}
	
	public void setVulnerRank(String vulnerRank){
		this.vulnerRank =  vulnerRank;
	}	

	public String getScriptName(){
		return scriptName;
	}
	
	public void setScriptName(String scriptName){
		this.scriptName =  scriptName;
	}	
	
	public String getScriptType(){
		return scriptType;
	}
	
	public void setScriptType(String scriptType){
		this.scriptType =  scriptType;
	}	
}
