package com.orleven.tentacle.define;

/**
 * 错误信息
 * @author orleven
 * @date 2017年3月18日
 */
public class Message {

	/**
	 * 验证成功
	 */
	public static final String AuthSuccess  = "[+] Auth success!";
	
	/**
	 * 网络连接超时
	 */
	public static final String Error = "[-] An error has occurred!";
	
	/**
	 * 网络连接超时
	 */
	public static final String ConnectionTimeOut  = "[-] Connection timed out!";
	

	/**
	 * 网络连接重置
	 */
	public static final String ConnectionReset  = "[-] Connection reset!";
	

	/**
	 * 网络连接终止
	 */
	public static final String ConnectionAbort  = "[-] Connection abort!";
	
	/**
	 * 网络连接被关闭
	 */
	public static final String ConnectionClosed  = "[-] Connection is closed!";
	
	/**
	 * 验证失败
	 */
	public static final String AuthFail  = "[-] Auth fail!";
	
	/**
	 * 漏洞不存在
	 */
	public static final String VulnerIsNoExist  = "[-] The vulner is not exist!";
	
	/**
	 * 漏洞不存在
	 */
	public static final String VulnerIsExist  = "[+] The vulner is exist!";
	
	/**
	 * 检测中
	 */
	public static final String VulnerIsChecking  = "[+] The vulner is checking!";
	
	/**
	 * 开始检测
	 */
	public static final String StartChecking  = "[+] Start checking!";
}
