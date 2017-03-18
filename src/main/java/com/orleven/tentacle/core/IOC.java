package com.orleven.tentacle.core;

import org.springframework.context.ApplicationContext;

import com.orleven.tentacle.entity.Vulner;

/**
 * IOC 类，便于管理所有的类
 * @author orleven
 * @date 2017年3月8日
 */
public class IOC {
	
	private static IOC ioc = new IOC();
	
	public static ApplicationContext  ctx;
	
	public static IOC instance() {
		if (ctx == null) {
			return null;
		}
		return ioc;
	}
	
	/**
	 * 获取ioc管理的类
	 * @param classObj
	 * @return
	 */
	public  <T> T getClassobj(Class<T> classObj){
		return IOC.ctx.getBean(classObj);
	}
	

}
