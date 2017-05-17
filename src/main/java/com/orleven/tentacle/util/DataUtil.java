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
