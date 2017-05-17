package com.orleven.tentacle.util;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import org.ini4j.InvalidFileFormatException;
import org.ini4j.Wini;



public class IniUtil {

	/**
	 * 获取所有配置
	 * @data 2017年5月13日
	 * @param iniPath
	 * @return
	 */
	public static Map<String,String> getConfig(String iniPath){
		Map<String,String>  config = new HashMap<String, String>();
        Wini ini;
		try {
			ini = new Wini(new File(iniPath));
			config.put("lhost", ini.get("Remote", "Local Host",String.class));
			config.put("lport", ini.get("Remote", "Local Port",String.class));
			config.put("rhost", ini.get("Remote", "Remote Host",String.class));
			config.put("rport", ini.get("Remote", "Remote Port",String.class));
			config.put("delay", ini.get("Remote", "HeartBeat Delay",String.class));
			return config;
		} catch (InvalidFileFormatException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}  

		config.put("lhost", "127.0.0.1");
		config.put("lport", "61234");
		config.put("rhost", "192.168.199.183");
		config.put("rport", "80");
		config.put("delay", "60" );
     	IniUtil.setConfig(config,"config/config.ini");
		return config;
	}
	
	/**
	 * 设置配置
	 * @data 2017年5月13日
	 * @param config
	 * @param iniPath
	 * @return
	 */
	public static boolean setConfig(Map<String,String>  config,String iniPath){
        Wini ini;
		try {
			File file = new File(iniPath);
			if(!file.exists()){
				file.createNewFile();
			}
			ini = new Wini(file);
			ini.setComment("Client configuration. \r\nTo avoid unnecessary coding problems, please use the English. \r\n\r\n");
			ini.putComment("Remote", "Configured to connect to the server. \r\n");
			ini.add("Remote", "Local Host",config.get("lhost"));
			ini.add("Remote", "Local Port",config.get("lport"));	
			ini.add("Remote", "Remote Host",config.get("rhost"));
			ini.add("Remote", "Remote Port",config.get("rport"));
			ini.add("Remote", "HeartBeat Delay",config.get("delay"));	
			ini.store();
		} catch (InvalidFileFormatException e) {
			e.printStackTrace();
			return false;
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}  
		return true;
	}
}
