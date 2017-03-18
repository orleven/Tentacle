package com.orleven.tentacle;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.embedded.ConfigurableEmbeddedServletContainer;
import org.springframework.boot.context.embedded.EmbeddedServletContainerCustomizer;
import org.springframework.boot.web.support.SpringBootServletInitializer;

import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.test.Test;

/**
 * 程序入口
 * @author orleven
 * @date 2017年3月8日
 */
@SpringBootApplication
public class TentacleApplication extends SpringBootServletInitializer implements EmbeddedServletContainerCustomizer {


	public static Log log = LogFactory.getLog(TentacleApplication.class);

	public static void main(String[] args) {
		// 启动Web服务
		IOC.ctx = SpringApplication.run(TentacleApplication.class, args);
		
		// 测试
		Test test = IOC.instance().getClassobj(Test.class);
		test.test();
	}

	@Override
	public void customize(ConfigurableEmbeddedServletContainer configurableEmbeddedServletContainer) {
		configurableEmbeddedServletContainer.setPort(61234);
	}

}
