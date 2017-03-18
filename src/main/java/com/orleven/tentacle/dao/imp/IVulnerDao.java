package com.orleven.tentacle.dao.imp;

import java.util.List;

import com.orleven.tentacle.entity.PasswordDic;
import com.orleven.tentacle.entity.Vulner;

/**
 * 漏洞库数据库接口
 * @author orleven
 * @date 2017年3月8日
 */
public interface IVulnerDao {
	/**
	 * 插入新的漏洞
	 * @param vulner
	 */
	public void insert(Vulner vulner);
	
	/**
	 * 获取所有的漏洞
	 * @return
	 */
	public List<Vulner> getAll();
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerId
	 * @return
	 */
	public Vulner getVulnerById(int vulnerId);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerCVE
	 * @return
	 */
	public Vulner getVulnerByCVE(int vulnerCVE);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerName
	 * @return
	 */
	public Vulner getVulnerByName(int vulnerName);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerRank
	 * @return
	 */
	public Vulner getVulnerByRank(int vulnerRank);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerType
	 * @return
	 */
	public Vulner getVulnerByType(int vulnerType);
}
