package com.orleven.tentacle.util;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import com.orleven.tentacle.define.Message;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * SSH 工具包
 * @author orleven
 * @date 2017年3月23日
 */
@Component
@Scope("prototype")
public class SshUtil {
	
	/**
	 * 登陆验证，并退出
	 * @data 2017年3月23日
	 * @param ip
	 * @param username
	 * @param password
	 * @param port
	 * @return
	 */
	public static String login(String ip,String username,String password,String port){
		Session session = null;
		JSch jsch=new JSch();
		String result = "";
		try {
			session = jsch.getSession(username, ip, Integer.valueOf(port).intValue());
			java.util.Properties config = new java.util.Properties();
			config.put("StrictHostKeyChecking", "no");
			session.setConfig(config);
			session.setPassword(password);
			session.connect();
		} catch (NumberFormatException e) {
			result += e.getMessage();
		} catch (JSchException e) {
			result += e.getMessage();
		} finally{
			if(session!=null&&session.isConnected()){
				session.disconnect();
				return Message.AuthSuccess;
			}
		}
		return result;
	}
	
	/**
	 * 登陆执行命令并退出
	 * @data 2017年3月23日
	 * @param ip
	 * @param username
	 * @param password
	 * @param port
	 * @param command
	 * @return
	 */
	public  static String loginExec(String ip,String username,String password,String port,String command){
		String result = "";
		Session session = null;
		ChannelExec openChannel =null;
		try {
			JSch jsch=new JSch();
			session = jsch.getSession(username, ip, Integer.valueOf(port).intValue());
			java.util.Properties config = new java.util.Properties();
			config.put("StrictHostKeyChecking", "no");
			session.setConfig(config);
			session.setPassword(password);
			session.connect();
			openChannel = (ChannelExec) session.openChannel("exec");
			openChannel.setCommand(command);
			openChannel.connect();  
            InputStream in = openChannel.getInputStream();  
            BufferedReader reader = new BufferedReader(new InputStreamReader(in));  
            String buf = null;
            while ((buf = reader.readLine()) != null) {
            	result+= new String(buf.getBytes("gbk"),"UTF-8")+"\n";  
            	
            }  
		} catch (JSchException | IOException e) {
			result+=e.getMessage();
		}finally{
			if(openChannel!=null&&!openChannel.isClosed()){
				openChannel.disconnect();
			}
			if(session!=null&&session.isConnected()){
				session.disconnect();
			}
		}
		return result;
	}
	
	/**
	 * SSH 长连接，不断开连接
	 * @data 2017年3月24日
	 * @param ip
	 * @param username
	 * @param password
	 * @param port
	 * @return
	 */
    public static Session connect(Session session,String ip, String username, String password,String port) {  
    	JSch jsch=new JSch();
        try {
			session = jsch.getSession(username, ip, Integer.valueOf(port).intValue());
	        session.setPassword(password);  
	        java.util.Properties config = new java.util.Properties();  
	        config.put("StrictHostKeyChecking", "no");  
	        session.setConfig(config);  
	        session.connect();  
		} catch (NumberFormatException e) {
			e.printStackTrace();
		} catch (JSchException e) {
			e.printStackTrace();
		}
		return session;
    }  
	
    /**
     * 长连接执行命令
     * @data 2017年3月24日
     * @param session
     * @param command
     * @return
     */
    public static String execCmd(Session session,String command){
        BufferedReader reader = null;  
        Channel channel = null;    
        String result = "";
        try {  
        	channel = session.openChannel("exec");  
            ((ChannelExec) channel).setCommand(command);  
              
            channel.setInputStream(null);  
            ((ChannelExec) channel).setErrStream(System.err);  

            channel.connect();  
            InputStream in = channel.getInputStream();  
            reader = new BufferedReader(new InputStreamReader(in));  
            String buf = null;  
            while ((buf = reader.readLine()) != null) {  
            	result+= new String(buf.getBytes("gbk"),"UTF-8")+"\n";  
            }  
        } catch (IOException e) {  
        	result+=e.getMessage();
        } catch (JSchException e) {  
        	result+=e.getMessage();
        } finally {  
            try {  
                reader.close();  
            } catch (IOException e) {  
                e.printStackTrace();  
            }  
            channel.disconnect();  
        }  
        return result;
    }  
    
    /**
     * 关闭长连接
     * @data 2017年3月24日
     * @param session
     * @return
     */
    public static boolean close(Session session){
        session.disconnect();  
        return true;
    }

}
