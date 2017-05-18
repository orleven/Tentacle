package com.orleven.tentacle.module.gather;

import java.util.ArrayList;
import java.util.List;

import org.nmap4j.Nmap4j;
import org.nmap4j.core.nmap.NMapExecutionException;
import org.nmap4j.core.nmap.NMapInitializationException;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.module.bean.AssetBean;

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
	 * 扫描运行标志
	 */
	private boolean runFlag ;
	
	public AssetGather(){
		this.nmapPath = "tools/windows/nmap";
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
	
	/**
	 * nmap自定义扫描,使用时请设置好nmap路径
	 * @data 2017年5月18日
	 * @param includeHosts
	 * @param excludeHosts
	 * @param flags
	 * @return
	 */
	public String nmapScan(String includeHosts,String excludeHosts,String flags){
		Nmap4j nmap4j = null ;	
		String result = null;
		try {
			nmap4j = new Nmap4j(this.nmapPath) ;
			nmap4j.includeHosts(includeHosts) ;
			nmap4j.excludeHosts(excludeHosts) ;
			nmap4j.addFlags(flags) ;
			nmap4j.execute();
			if(!nmap4j.hasError() ) {
				result = nmap4j.getOutput();
			}else{
				 System.out.println( nmap4j.getExecutionResults().getErrors() ) ;
			}
		} catch (NMapInitializationException e) {
			e.printStackTrace();
		} catch (NMapExecutionException e) {
			e.printStackTrace();
		}
		return result;
	}
	
	/**
	 * 全方面全端口扫描
	 * @data 2017年5月18日
	 * @return
	 */
	public List<AssetBean> FullScan(){
		List<AssetBean> assetBeans = null;
		
//		assetBeans = new ArrayList<AssetBean>();
		
		return assetBeans;
	}
	


	
}
