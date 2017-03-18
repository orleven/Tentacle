package com.orleven.tentacle.permeate.script;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.permeate.script.base.WebScriptBase;

/**
 * Struts2 RCE 032
 * @author orleven
 * @date 2017年3月19日
 */
@Component
@Scope("prototype")
public class Struts2RCE032 extends WebScriptBase{
	
	public Struts2RCE032(){
		super();
	}
	
	@Override
	public void prove() {
		
	}
	
	@Override
	public void execCommand(String command) {
		
	}
}
