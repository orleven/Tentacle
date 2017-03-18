package com.orleven.tentacle.permeate.script.imp;

/**
 * 漏洞验证接口,验证漏洞是否存在
 * @author orleven
 * @time  2016年12月15日
 */
public interface ProveImp {
	/**
	 * 检测漏洞是否存在，返回检测结果以及存在的取证数据，取证据式扫描有取证数据，一定要返回。
	 * @return
	 */
	public void prove();

}
