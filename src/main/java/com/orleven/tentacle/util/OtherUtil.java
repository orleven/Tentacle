package com.orleven.tentacle.util;

import java.text.DateFormat;
import java.util.Date;

/**
 * 杂类工具包
 * @author orleven
 * @date 2017年3月24日
 */
public class OtherUtil {
	
    /**
     * 获取当前的时间 
     */
    public static String getTime() {
    	return DateFormat.getDateTimeInstance().format(new Date());
    }
    
    /**
     * 获取当前的时间戳
     * @return
     */
    public static String getTimeStamp() {
    	return String.valueOf(new Date().getTime());
    }
}
