package com.orleven.tentacle.config;

import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

/**
 * 线程池配置
 * @author orleven
 * @date 2017年5月16日
 */
@Configuration  
@EnableAsync  
public class ExecutorConfig {
	/**
	 * 设置ThreadPoolExecutor的核心池大小 
	 */
    private int corePoolSize = 10;  
    
    /**
     * 设置线程池的最大池大小
     */
    private int maxPoolSize = 200;  
    
    /**
     * 设置ThreadPoolExecutor的BlockingQueue
     */
    private int queueCapacity = 10;  
  
    /**
     * 异步配置测试
     * @data 2017年5月16日
     * @return
     */
    @Bean  
    public Executor myAsyncTest() {  
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();  
        executor.setCorePoolSize(corePoolSize);  
        executor.setMaxPoolSize(maxPoolSize);  
        executor.setQueueCapacity(queueCapacity);  
        executor.setThreadNamePrefix("MySimpleExecutor-");  
        executor.initialize();  
        return executor;  
    }  
    
    /**
     * 异步配置
     * @data 2017年5月16日
     * @return
     */
    @Bean  
    public Executor myAsync() {  
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();  
        executor.setCorePoolSize(corePoolSize);  
        executor.setMaxPoolSize(maxPoolSize);  
        executor.setQueueCapacity(queueCapacity);  
        executor.setThreadNamePrefix("MyExecutorUnit-");  
  
        // rejection-policy：当pool已经达到max size的时候，如何处理新任务  
        // CALLER_RUNS：不在新线程中执行任务，而是有调用者所在的线程来执行  
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());  
        executor.initialize();  
        return executor;  
    }  
}
