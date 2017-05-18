package com.orleven.tentacle.module.gather;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import org.nmap4j.Nmap4j;
import org.nmap4j.core.nmap.ExecutionResults;
import org.nmap4j.core.nmap.NMapExecutionException;
import org.nmap4j.core.nmap.NMapInitializationException;
import org.nmap4j.data.NMapRun;
import org.nmap4j.data.nmaprun.Host;
import org.springframework.stereotype.Component;

/**
 * 资产扫描模块
 * @author orleven
 * @date 2017年5月17日
 */
@Component
public class AssetGather {
	
	/**
	 * nmap地址 后面自动填充 /bin/nmap
	 * 所以加入nmap地址为 tools\windows\nmap\bin\nmap.exe
	 * 则需要填写tools/windows/nmap，并复制nmap.exe 重命名为nmap
	 */
	private String nmapPath ;
	/**
	 * 扫描间隔 30毫秒发包 --scan-delay 30ms
	 */
	private String scanDelayFlag ;
	
	/**
	 * 扫描方式
	 */
	private Map<String,String> flags ;
	
	public AssetGather(){
		this.nmapPath = "tools/windows/nmap";
		this.scanDelayFlag = "";
		this.flags = new HashMap();
		this.flags.put("SpeedSystemScan", " -T4 -O -oX ");
//		this.flags.put("PortScan", " -T4 -O -oX ");
//		this.flags.put("SpeedPortScan", " -T4  -oX ");
		this.flags.put("Speed1000PortScan", " -T4  -oX ");
		this.flags.put("SpeedAllPortScan", " -T4 -p- -oX ");
	}

	public void test(){
		 Nmap4j nmap4j = null ;		 
		 try {
			 nmap4j = new Nmap4j( "tools/windows/nmap" ) ;	
			 nmap4j.includeHosts( "192.168.199.130" ) ;
//			 nmap4j.excludeHosts( "192.168.199.129" ) ;
			 nmap4j.addFlags( "-oX -O -T4" ) ;
			 nmap4j.execute();
			 if(!nmap4j.hasError() ) {
				 System.out.println(nmap4j.getOutput()) ;
			 } else {
				 System.out.println( nmap4j.getExecutionResults().getErrors() ) ;
			 }
		 } catch (NMapInitializationException e) {
				e.printStackTrace();
		 } catch (NMapExecutionException e) {
				e.printStackTrace();
		 }
	}

	/**
	 * 设置nmap路径
	 * nmap地址 后面自动填充 /bin/nmap
	 * 所以加入nmap地址为 tools\windows\nmap\bin\nmap.exe
	 * 则需要填写tools/windows/nmap，并复制nmap.exe 重命名为nmap
	 * @data 2017年5月17日
	 * @param nmapPath
	 */
	public void setNmapPath(String nmapPath){
		this.nmapPath = nmapPath ;
	}
	
	public void setScanDelayFlag(String scanDelayFlag){
		this.scanDelayFlag = " --scan-delay " + scanDelayFlag+" " ;
	}
}
