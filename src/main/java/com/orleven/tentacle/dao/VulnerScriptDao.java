package com.orleven.tentacle.dao;

import java.util.List;
import com.orleven.tentacle.entity.VulnerScript;

/**
 * 漏洞库数据库接口
 * @author orleven
 * @date 2017年3月8日
 */
public interface VulnerScriptDao {
	

	/**
	 * 创建表
	 * @data 2017年3月19日
	 * @return
	 * @throws Exception
	 */
	public boolean createTable() throws Exception ;
	
	/**
	 * 插入新的漏洞
	 * @param vulner
	 */
	public boolean insert(VulnerScript vulnerScript);
	
	/**
	 * 获取所有的漏洞
	 * @return
	 */
	public List<VulnerScript> getAll();
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerId
	 * @return
	 */
	public VulnerScript getVulnerById(int vulnerId);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerCVE
	 * @return
	 */
	public VulnerScript getVulnerByCVE(String vulnerCVE);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerName
	 * @return
	 */
	public VulnerScript getVulnerByName(String vulnerName);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerRank
	 * @return
	 */
	public VulnerScript getVulnerByRank(String vulnerRank);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerType
	 * @return
	 */
	public VulnerScript getVulnerByType(String vulnerType);
}
