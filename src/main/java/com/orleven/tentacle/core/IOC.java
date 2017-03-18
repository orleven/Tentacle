package com.orleven.tentacle.core;

import org.springframework.context.ApplicationContext;

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
	
	/**
	 * 根据类名获取类
	 * @param className
	 * @return
	 */
	public  Object getClassobj(String className){
		return IOC.ctx.getBean(className);
	}
	
	/**
	 * 获取所有bean名称
	 * @return
	 */
	public String[] getAllBean(){
		return IOC.ctx.getBeanDefinitionNames();
	}

}
