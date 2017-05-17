package com.orleven.tentacle.core;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ScheduledThread {
    
    public ScheduledThread(){

    }
    
   
    /**
     * 默认一分钟执行一次
     * @data 2017年5月15日
     */
    @Scheduled(fixedDelay=60*1000) 
    public void task() {

    }
    
}
