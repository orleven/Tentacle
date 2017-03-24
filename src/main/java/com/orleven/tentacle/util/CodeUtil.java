package com.orleven.tentacle.util;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.io.IOUtils;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

/**
 * 编码工具包
 * @author orleven
 * @date 2017年3月22日
 */
public class CodeUtil {
	
    /**
     * 计算字符串MD5
     * @param str
     * @return
     */
    public static String getMD5(String str) {
        String md5 = null;
		md5 = DigestUtils.md5Hex(str.getBytes());
        return md5;
    }
    
    /**
     * 计算byte  MD5
     * @param byt
     * @return
     */
    public static String getMD5(byte[] byt) {
        String md5 = null;
		md5 = DigestUtils.md5Hex(byt);
        return md5;
    }
    
    /**
     * 计算文件MD5
     * @param file
     * @return
     */
    public static String getMd5ByFile(File file) {
        String md5 = null;
        FileInputStream fis = null;
		try {
			fis = new FileInputStream(file);
			md5 = DigestUtils.md5Hex(IOUtils.toByteArray(fis));
	        IOUtils.closeQuietly(fis); 
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}    
        return md5;
    }
    
    /**
     * 计算字符串Sha1
     * @param str
     * @return
     */
    public static String getSHA1(String str) {
        String md5 = null;
		md5 = DigestUtils.sha1Hex(str.getBytes());
        return md5;
    }
    
    /**
     * 计算byte  Sha1
     * @param byt
     * @return
     */
    public static String getSHA1(byte[] byt) {
        String md5 = null;
		md5 = DigestUtils.sha1Hex(byt);
        return md5;
    }
    
    /**
     * 计算文件Sha1
     * @param file
     * @return
     */
    public static String getSHA1ByFile(File file) {
        String md5 = null;
        FileInputStream fis = null;
		try {
			fis = new FileInputStream(file);
			md5 = DigestUtils.sha1Hex(IOUtils.toByteArray(fis));
	        IOUtils.closeQuietly(fis); 
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}    
        return md5;
    }
	
	/**
	 * 转json
	 * @param params
	 * @return
	 */
    public static String toJson(Map params){
        Gson gson=new Gson();
        return gson.toJson(params);
    }

    /**
     * json转map
     * @param jsonStr
     * @return
     */
    public static HashMap<String,Object> fromJson(String jsonStr){
        Gson gson=new Gson();
        Type type=new TypeToken<HashMap<String,Object>>(){}.getType();
        return gson.fromJson(jsonStr,type);
    }
}
