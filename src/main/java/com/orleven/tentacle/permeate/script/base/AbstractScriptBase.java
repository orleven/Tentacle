package com.orleven.tentacle.permeate.script.base;



import com.orleven.tentacle.permeate.bean.AssetInfoBean;
import com.orleven.tentacle.permeate.bean.VulnerBean;


/**
 * 针对某个漏洞的虚拟利用基础类
 * @author orleven
 * @time  2016年12月15日
 */
public abstract class AbstractScriptBase{
	
	/**
	 * 资产基础信息
	 */
	private AssetInfoBean assetInfoBean ;

	/**
	 * 漏洞信息
	 */
	private VulnerBean vulnerBean;

//	/**
//	 * 链接目的的超时时间
//	 */
//	private int connectTimeout;    
	
//	/**
//	 * 是否设置代理
//	 */
//	private boolean isProxy ;    
	

//	/**
//	 * 当前请求数量,保证线程安全
//	 */
//	private static AtomicInteger currentCount ;
//	
//	/**
//	 * 总请求数量
//	 */
//	private int totalCount;
//	
	public AbstractScriptBase(){
		vulnerBean = new VulnerBean();
	}
	
	public void setVulnerBean(VulnerBean vulnerBean){
		this.vulnerBean =  vulnerBean;
	}
	
	public VulnerBean getVulnerBean(){
		return vulnerBean;
	}

//	public void setIsProxy(boolean isProxy) {
//		this.isProxy = isProxy;
//	}
	
//	public boolean IsProxy() {
//		return isProxy;
//	}
	
	public void setAssetInfoBean(AssetInfoBean assetInfoBean){
		this.assetInfoBean = assetInfoBean;
	}
	
	public AssetInfoBean getAssetInfoBean(){
		return assetInfoBean;
	}


//	public void setCurrentCount(AtomicInteger currentCount) {
//		this.currentCount = currentCount;
//	}
//	
//	public AtomicInteger getCurrentCount() {
//		return currentCount;
//	}
//	public void setTotalCount(int totalCount) {
//		this.totalCount = totalCount;
//	}
//	
//	public int getTotalCount() {
//		return totalCount;
//	}
	
//	/**
//	 * 返回当前poc进度
//	 * @return
//	 */
//	public String getSchedule() {
//		String str = "("+currentCount.get()+"/"+totalCount+")";
//		return str;
//	}
}
