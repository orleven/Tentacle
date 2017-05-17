package com.orleven.tentacle.util;

import java.io.File;
import java.lang.reflect.Type;
import java.text.DateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

//import com.google.gson.Gson;
//import com.google.gson.reflect.TypeToken;

public class DataUtil {
	
	/**
	 * 获取时间
	 * @data 2017年5月13日
	 * @return
	 */
	public static String getTime() {
		return DateFormat.getDateTimeInstance().format(new Date());
	}
   
	/**
	 * 获取时间戳
	 * @data 2017年5月13日
	 * @return
	 */
	public static String getTimeStamp() {
   		return String.valueOf(new Date().getTime()).substring(0,10);
	}
	
	/**
	 * 去重
	 * @data 2017年5月13日
	 * @param arrayList
	 * @return
	 */
    public static String[] removeDuplicate(String[] arrayList){
        Set<String> set = new HashSet<>();  
        for(int i=0;i<arrayList.length;i++){  
        	if(arrayList[i]!=null&&!arrayList[i].equals("")){
        		set.add(arrayList[i]); 
        	}
        }  
        return (String[]) set.toArray(new String[set.size()]);  
    }

    /**
     * 操作系统斜杆处理
     * @data 2017年5月13日
     * @param text
     * @return
     */
    public static String slashDeal(String text){
    	if(File.separator.equals("\\")){
    		text = text.replaceAll("/", "\\\\");
    	}else{
    		text = text.replaceAll("\\\\", "/");
    	}
    	return text;
    }
    
    /**
     * 换行处理
     * @data 2017年5月13日
     * @param text
     * @return
     */
    public static String removeLinefeed(String text){
    	text = text.replaceAll("\r", "").replaceAll("\n", "");
    	return text;
    }
    
    /**
     * ip地址转化为数字
     * @data 2017年5月17日
     * @param ipAddress
     * @return
     */
    public static long ipToLong(String ipAddress) {  
    	  
        String[] addrArray = ipAddress.split("\\.");  
  
        long num = 0;  
        for (int i = 0; i < addrArray.length; i++) {  
  
            int power = 3 - i;  
  
            // 1. (192 % 256) * 256 pow 3  
            // 2. (168 % 256) * 256 pow 2  
            // 3. (108 % 256) * 256 pow 1  
            // 4. (108 % 256) * 256 pow 0  
            num += ((Integer.parseInt(addrArray[i]) % 256 * Math  
                    .pow(256, power)));  
  
        }  
        return num;  
    }  
  
    /**
     * 把数字转化为ip
     * @data 2017年5月17日
     * @param i
     * @return
     */
    public static String longToIp(long i) {  
        return ((i >> 24) & 0xFF) + "." + ((i >> 16) & 0xFF) + "."  
                + ((i >> 8) & 0xFF) + "." + (i & 0xFF);  
    }  
  
    /**
     * 打印漂亮二进制代码，填充左零
     * @data 2017年5月17日
     * @param binary
     */
    private static void printPrettyBinary(String binary) {  
        String s1 = String.format("%32s", binary).replace(' ', '0');  
        System.out.format("%8s %8s %8s %8s %n", s1.substring(0, 8), s1  
                .substring(8, 16), s1.substring(16, 24), s1.substring(24, 32));  
    }  
    
//    /**
//     * Map trans to Json
//     * @param params
//     * @return String
//     */
//    public static String toJson(Map params){
//        Gson gson=new Gson();
//        return gson.toJson(params);
//    }
//
//    /**
//     * 
//     * @data 2017��4��24��
//     * @param params
//     * @return
//     */
//    public static String toJson(Object src){
//        Gson gson=new Gson();
//        return gson.toJson(src);
//    }
//
//    
//    public static Object fromJsonToObject(String jsonStr){
//        Gson gson=new Gson();
//        Type type=new TypeToken<Object>(){}.getType();
//        return gson.fromJson(jsonStr,type);
//    }
//    
//    /**
//     * Json string to HashMap<String,Object>
//     * @param jsonStr
//     * @return HashMap<String,Object>
//     */
//    public static HashMap<String,Object> fromJson(String jsonStr){
//    	Gson gson=new Gson();
//    	Type type=new TypeToken<HashMap<String,Object>>(){}.getType();
//
//        return gson.fromJson(jsonStr,type);
//    }
}
