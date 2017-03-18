package com.orleven.tentacle.permeate.script.imp;

/**
 * 清除相关临时文件、进程、日志等
 * @author orleven
 * @time  2016年12月15日
 */
public interface DestroyImp {
	/**
	 * 用于删除或者释放写入被测试系统的临时文件、进程、日志等等
	 */
	public void destroy();
}