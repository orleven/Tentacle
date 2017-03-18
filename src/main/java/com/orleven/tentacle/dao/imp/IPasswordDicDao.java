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
	 * 插入新的密码
	 * @param passwordDic
	 */
	public void insert(PasswordDic passwordDic);
	
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
