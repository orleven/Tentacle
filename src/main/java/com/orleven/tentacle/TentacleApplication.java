package com.orleven.tentacle;

import org.apache.commons.logging.LogFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.embedded.ConfigurableEmbeddedServletContainer;
import org.springframework.boot.context.embedded.EmbeddedServletContainerCustomizer;
import org.springframework.boot.web.support.SpringBootServletInitializer;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;
import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.module.pentest.test.ModulePentestTest;
import com.orleven.tentacle.core.ControllerCenter;


/**
 * 程序入口
 * @author orleven
 * @date 2017年3月8日
 */
@EnableAsync  
@EnableScheduling
@SpringBootApplication
public class TentacleApplication extends SpringBootServletInitializer implements EmbeddedServletContainerCustomizer {

	public static void main(String[] args) {
		IOC.log = LogFactory.getLog(TentacleApplication.class);
		IOC.ctx = SpringApplication.run(TentacleApplication.class, args);
		ControllerCenter controllerCenter = IOC.ctx.getBean(ControllerCenter.class);
		controllerCenter.work();
		
		// 测试
		ModulePentestTest modulePentestTest = IOC.ctx.getBean(ModulePentestTest.class);
//		modulePentestTest.init();
//		modulePentestTest.scriptTest();
		
		modulePentestTest.sshUnitTest();
		
	}

	@Override
	public void customize(ConfigurableEmbeddedServletContainer configurableEmbeddedServletContainer) {
		configurableEmbeddedServletContainer.setPort(61234);
	}

}
