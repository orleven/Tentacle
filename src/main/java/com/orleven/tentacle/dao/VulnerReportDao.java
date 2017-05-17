package com.orleven.tentacle.dao;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

import com.orleven.tentacle.entity.VulnerReport;


public interface VulnerReportDao {
	/**
	 * 创建表
	 * @data 2017年3月19日
	 * @return
	 * @throws Exception
	 */
	public boolean createTable() ;
	
	/**
	 * 插入新的漏洞
	 * @param vulner
	 */
	public boolean insert(VulnerReport vulnerReport);
	
	/**
	 * 获取所有的漏洞
	 * @return
	 */
	public List<VulnerReport> getAll();
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerId
	 * @return
	 */
	public VulnerReport getReportById(int reportId);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerCVE
	 * @return
	 */
	public VulnerReport getReportByVulnerId(String VulnerId);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerName
	 * @return
	 */
	public VulnerReport getReportByHost(String host);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerRank
	 * @return
	 */
	public VulnerReport getReportByPort(String port);
	
	/**
	 * 取出特定的漏洞
	 * @param vulnerType
	 * @return
	 */
	public VulnerReport getReportByIndex(String index);
	
	/**
	 * 表格存在
	 * @data 2017年5月17日
	 * @return
	 * @throws Exception
	 */
	public boolean isTableExist() ;

	/**
	 * 删除所有
	 * @data 2017年5月17日
	 * @return
	 * @throws Exception
	 */
	public boolean deleteAll();

	/**
	 * 删除表
	 * @data 2017年5月17日
	 * @return
	 * @throws Exception
	 */
	public boolean deleteTable();
	
	/**
	 * 关闭连接
	 * @data 2017年5月17日
	 * @return
	 */
	public boolean closeConnection();
	
	/**
	 * 开启连接
	 * @data 2017年5月17日
	 * @return
	 */
	public boolean connectDB();
}
