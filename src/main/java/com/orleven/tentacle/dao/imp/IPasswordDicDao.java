package com.orleven.tentacle.dao.imp;

import java.util.List;

import com.orleven.tentacle.entity.PasswordDic;

/**
 * Password 字典接口
 * @author orleven
 * @date 2017年3月8日
 */
public interface  IPasswordDicDao {
	
	/**
	 * 创建表
	 * @data 2017年3月19日
	 * @return
	 * @throws Exception
	 */
	public boolean createTable() throws Exception ;
	
	/**
	 * 插入新的密码
	 * @param passwordDic
	 */
	public boolean insert(PasswordDic passwordDic);
	
	/**
	 * 获取所有的密码
	 * @return
	 */
	public List<PasswordDic> getAll();
	
	/**
	 * 取出特定的密码
	 * @param id
	 * @return
	 */
	public PasswordDic getPasswordById(int id);
}
