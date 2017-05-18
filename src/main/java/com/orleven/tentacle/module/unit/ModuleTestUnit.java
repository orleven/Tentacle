package com.orleven.tentacle.module.unit;

import java.util.concurrent.Future;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Component;
import com.orleven.tentacle.core.IOC;

/**
 * 测试单元（线程）
 * @author orleven
 * @date 2017年5月15日
 */
@Component  
public class ModuleTestUnit {

	/**
	 * 单元测试
	 * @data 2017年5月16日
	 * @return
	 * @throws InterruptedException
	 */
    @Async("myAsync")  
    public Future<String> doUnitTest() throws InterruptedException{  
    	IOC.log.info("Unit Test started.");
        long start = System.currentTimeMillis();  
        Thread.sleep(3000);  
        long end = System.currentTimeMillis();  
        IOC.log.info("Unit Test finished, time elapsed: " + Long.toString(end-start) +" ms.");        
        return new AsyncResult<>("Unit Test accomplished!");  
    }  
    
    
}
