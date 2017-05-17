package com.orleven.tentacle.entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

/**
 * VulnerReport 主要收集资产的漏洞
 * @author orleven
 * @date 2017年5月16日
 */
@Entity
@Table(name="VulnerReport")
public class VulnerReport {
	
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ReportId") 
	private int reportId;
    
    
    /**
     * 漏洞主机
     */
    private String host;
    
    /**
     * 漏洞端口
     */
    private String port;
    
    /**
     * 端口类型
     */
    private String type;
    
    /**
     * 索引，便于根进行查找，index的机制： 数字型ip数字型ip数字型ip数字型ip...
     */
    private String index;
    
    /**
     * 对应的脚本id
     */
    private int VulnerId;
    
    
    
}
