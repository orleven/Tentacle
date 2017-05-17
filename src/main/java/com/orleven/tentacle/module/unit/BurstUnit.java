package com.orleven.tentacle.module.unit;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Future;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.dao.imp.VulnerScriptDaoImp;
import com.orleven.tentacle.define.Permeate;
import com.orleven.tentacle.entity.VulnerScript;
import com.orleven.tentacle.module.bean.SshServiceBean;
import com.orleven.tentacle.module.common.BurstDictionary;
import com.orleven.tentacle.module.pentest.SshAbstractScript;
import com.orleven.tentacle.module.pentest.script.SshWeakBurst;
import com.orleven.tentacle.util.FileUtil;

/**
 * 爆破单元（线程）
 * @author orleven
 * @date 2017年5月16日
 */
@Component  
public class BurstUnit {
	
	@Autowired
	private VulnerScriptDaoImp vulnerDaoImp;
	/**
	 * 字典
	 */
	@Autowired
	private BurstDictionary burstDictionary;
	
//	public void init(String usernameDic,String passwordDic,String pathDic){
//		burstDictionary.load(usernameDic, passwordDic, pathDic);
//	}
 
	/**
	 * SSH 爆破单元
	 * @data 2017年5月16日
	 * @return
	 * @throws InterruptedException
	 */
    @Async("myAsync")   
    public Future<Boolean> doSShPasswordBurstUnit(SshServiceBean sshServiceBean,int start, int end) throws InterruptedException{  
    	SshWeakBurst sshWeakBurst =  IOC.ctx.getBean(SshWeakBurst.class);
    	sshWeakBurst.setSshServiceBean(sshServiceBean);
    	sshWeakBurst.setUsername("orleven");
    	sshWeakBurst.getVulnerBean().setVulner(vulnerDaoImp.getVulnerByName("SSHWeakBurst"));
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
}
