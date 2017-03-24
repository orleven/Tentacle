package com.orleven.tentacle.permeate.script;

import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.define.Message;
import com.orleven.tentacle.define.Permeate;
import com.orleven.tentacle.permeate.bean.ProveBean;
import com.orleven.tentacle.permeate.script.base.SshScriptBase;
import com.orleven.tentacle.util.SshUtil;

/**
 * SSH 端口爆破
 * @author orleven
 * @date 2017年3月22日
 */
public class SshWeakBurst extends SshScriptBase{
	
	public SshWeakBurst(){
		super();
	}
	
	@Override
	public void prove() {
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String result = SshUtil.login(getAssetInfoBean().getHost(), getUsername(), getPassword(), getSshServiceBean().getPort());
		if (result.indexOf(Message.AuthSuccess)>=0){
			getVulnerBean().setIsVulner(Permeate.isVulner);
		}else{
			getVulnerBean().setIsVulner(Permeate.isNotVerified);
		}
		proveBean.setReceiveMessage(result);
		proveBean.setSendMessage("Username : "+ getUsername() + "\r\nPassword : " +getPassword());
		getVulnerBean().getProveBean().add(proveBean);
	}
	
	@Override
	public void execCommand(String command) {
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String result = SshUtil.loginExec(getAssetInfoBean().getHost(), getUsername(), getPassword(), getSshServiceBean().getPort(),command);
		proveBean.setReceiveMessage(result);
		proveBean.setSendMessage("command : " + command);
		getVulnerBean().getProveBean().add(proveBean);
	}
	

	@Override
	public void uploadFile(String inFile,String outFile) {
		
	}
}
