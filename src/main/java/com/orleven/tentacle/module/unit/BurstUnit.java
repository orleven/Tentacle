package com.orleven.tentacle.module.unit;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Future;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.dao.imp.VulnerReportDaoImp;
import com.orleven.tentacle.dao.imp.VulnerScriptDaoImp;
import com.orleven.tentacle.define.Permeate;
import com.orleven.tentacle.entity.VulnerScript;
import com.orleven.tentacle.module.bean.SshServiceBean;
import com.orleven.tentacle.module.common.BurstDictionary;
import com.orleven.tentacle.module.pentest.SshAbstractScript;
import com.orleven.tentacle.module.pentest.script.SshWeakBurst;
import com.orleven.tentacle.util.FileUtil;

/**
 * 爆破单元（线程），即一个脚本多个线程
 * @author orleven
 * @date 2017年5月16日
 */
@Component  
public class BurstUnit {
	
	@Autowired
	private VulnerScriptDaoImp vulnerScriptDaoImp;
	
//	@Autowired
//	private VulnerReportDaoImp vulnerReportDaoImp;
	
	/**
	 * 字典
	 */
	@Autowired
	private BurstDictionary burstDictionary;
	
 
	/**
	 * 单个ip SSH 密码字典爆破单元
	 * @data 2017年5月17日
	 * @param sshServiceBean
	 * @param start
	 * @param end
	 * @param username
	 * @return
	 * @throws InterruptedException
	 */
    @Async("myAsync")   
    public Future<Boolean> doOneSShPasswordDicBurstUnit(SshServiceBean sshServiceBean,int start, int end,String username) throws InterruptedException{  
    	SshWeakBurst sshWeakBurst =  IOC.ctx.getBean(SshWeakBurst.class);
    	sshWeakBurst.setSshServiceBean(sshServiceBean);
    	sshWeakBurst.setUsername(username);
    	sshWeakBurst.getVulnerBean().setVulner(vulnerScriptDaoImp.getVulnerByName("SSHWeakBurst"));
    	List<String> passwords = burstDictionary.getPasswords();
    	for(int i = start;i < end && i < passwords.size() ;i ++ ){
    		sshWeakBurst.setPassword(passwords.get(i));
    		sshWeakBurst.prove();
    		sshWeakBurst.setCurrentCount(sshWeakBurst.getCurrentCount()+1);;
    		if(sshWeakBurst.getVulnerBean().getIsVulner() == Permeate.isVulner){
    			return new AsyncResult<>(true);  
    		}
    	}
        return new AsyncResult<>(false);  
    }  
    
    /**
     * 多个ip SSH 单一用户密码爆破
     * @data 2017年5月17日
     * @param sshServiceBeans
     * @param start
     * @param end
     * @param username
     * @param password
     * @return
     * @throws InterruptedException
     */
    @Async("myAsync")   
    public Future<Boolean> doMulSShSimpleBurstUnit(List<SshServiceBean> sshServiceBeans,int start, int end,String username,String password) throws InterruptedException{  
    	SshWeakBurst sshWeakBurst =  IOC.ctx.getBean(SshWeakBurst.class);
    	sshWeakBurst.setUsername(username);
    	sshWeakBurst.setPassword(password);
    	sshWeakBurst.getVulnerBean().setVulner(vulnerScriptDaoImp.getVulnerByName("SSHWeakBurst"));
    	for(int i = start;i < end && i < sshServiceBeans.size() ;i ++ ){
    		sshWeakBurst.setSshServiceBean(sshServiceBeans.get(i));
    		sshWeakBurst.prove();
    		sshWeakBurst.setCurrentCount(sshWeakBurst.getCurrentCount()+1);;
    	}
        return new AsyncResult<>(true);  
    }  
}
