package com.orleven.tentacle.util;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.lang.reflect.Type;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.codec.digest.DigestUtils;
import org.apache.tomcat.util.http.fileupload.IOUtils;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import sun.misc.BASE64Decoder;
import sun.misc.BASE64Encoder;

/**
 * 编码工具包
 * @author orleven
 * @date 2017年3月22日
 */
public class CodeUtil {
	/**
     * base64 解密
     * @data 2017年5月3日
     * @param text
     * @return
     */
    public static byte[] base64Decode(String text)
    {
    	byte[] b = null;  
        try {  
            b = new BASE64Decoder().decodeBuffer(text);  
        } catch (Exception e) {  
            e.printStackTrace();  
        }  
        return b;
    }
    
    /**
     * base64 加密
     * @data 2017年5月3日
     * @param text
     * @return
     */
    public static String base64Encode(byte[] text)
    {
        return new BASE64Encoder().encode(text);
    }
    
    /**
     * url 加密
     * @data 2017年5月3日
     * @param text
     * @return
     */
    public static String urlEncode(String text){
    	try {
    		text = URLEncoder.encode(text, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}  
    	return text;
    }
    
    /**
     * url 解密
     * @data 2017年5月3日
     * @param text
     * @return
     */
    public static String urlDecode(String text){
    	try {
    		text = URLDecoder.decode(text, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}  
    	return text;
    }
    
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
     * @author orleven
     * @param file
     * @return
     */
//    public static String getMd5ByFile(File file) {
//        String md5 = null;
//        FileInputStream fis = null;
//		try {
//			fis = new FileInputStream(file);
//			md5 = DigestUtils.md5Hex(IOUtils.toByteArray(fis));
//	        IOUtils.closeQuietly(fis); 
//		} catch (FileNotFoundException e) {
//			e.printStackTrace();
//		} catch (IOException e) {
//			e.printStackTrace();
//		}    
//        return md5;
//    }
    
    /**
     * 计算字符串Sha1
     * @author orleven
     * @param str
     * @return
     */
    public static String getSHA1(String str) {
        return DigestUtils.sha1Hex(str.getBytes());
    }
    
    /**
     * 计算byte  Sha1
     * @param byt
     * @return
     */
    public static String getSHA1(byte[] byt) {
        return DigestUtils.sha1Hex(byt);
    }
    
    /**
     * 计算文件Sha1
     * @author orleven
     * @param file
     * @return
     */
//    public static String getSHA1ByFile(File file) {
//        String md5 = null;
//        FileInputStream fis = null;
//		try {
//			fis = new FileInputStream(file);
//			md5 = DigestUtils.sha1Hex(IOUtils.toByteArray(fis));
//	        IOUtils.closeQuietly(fis); 
//		} catch (FileNotFoundException e) {
//		} catch (IOException e) {
//		}    
//        return md5;
//    }
}
