package com.orleven.tentacle.util;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.ParseException;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpOptions;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpHead;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;


/**
 * 发送接收HTTP请求工具包
 * @author orleven
 * @date 2017年3月8日
 */
@Component
@Scope("prototype")
public class WebUtil {
	
	/**
	 * post 方法
	 * @param targetUrl
	 * @param httpHeaders
	 * @param postParameters
	 */
	public static HttpResponse httpPost(String targetUrl,Map<String, String> httpHeaders,List<BasicNameValuePair> postParameters){
		HttpClient client = HttpClients.createDefault();
		HttpPost post = new HttpPost(targetUrl);
		for (String key : httpHeaders.keySet()) {
        	post.setHeader(key, httpHeaders.get(key));
        }
        try {
			post.setEntity(new UrlEncodedFormEntity(postParameters, "utf-8"));
			return client.execute(post);
		} catch (UnsupportedEncodingException e) {
//			e.printStackTrace();
		} catch (ClientProtocolException e) {
//			e.printStackTrace();
		} catch (IOException e) {
//			e.printStackTrace();
		}
		return null;
	}
	
	/**
	 * post 方法
	 * @param targetUrl
	 * @param httpHeaders
	 * @param postParameters
	 */
	public static HttpResponse httpPost(String targetUrl,Map<String, String> httpHeaders,byte[] postParameters){
		HttpClient client = HttpClients.createDefault();
		HttpPost post = new HttpPost(targetUrl);
		for (String key : httpHeaders.keySet()) {
        	post.setHeader(key, httpHeaders.get(key));
        }
        try {
        	post.setEntity(new ByteArrayEntity(postParameters));
        	return client.execute(post);
		} catch (UnsupportedEncodingException e) {
//			e.printStackTrace();
		} catch (ClientProtocolException e) {
//			e.printStackTrace();
		} catch (IOException e) {
//			e.printStackTrace();
		}
		return null;

	}
	
	
	/**
	 * post 方法
	 * @param targetUrl
	 * @param httpHeaders
	 * @param postParameters
	 */
	public static HttpResponse httpPost(String targetUrl,Map<String, String> httpHeaders,String postParameters){
		HttpClient client = HttpClients.createDefault();
		HttpPost post = new HttpPost(targetUrl);
		for (String key : httpHeaders.keySet()) {
        	post.setHeader(key, httpHeaders.get(key));
        }
        try {
        	post.setEntity(new StringEntity(postParameters));
        	return client.execute(post);
		} catch (UnsupportedEncodingException e) {
//			e.printStackTrace();
		} catch (ClientProtocolException e) {
//			e.printStackTrace();
		} catch (IOException e) {
//			e.printStackTrace();
		}
		return null;

	}
	
	/**
	 * get 方法
	 * @param targetUrl
	 * @param httpHeaders
	 */
	public static HttpResponse httpGet(String targetUrl,Map<String, String> httpHeaders){
		HttpClient client = HttpClients.createDefault();
		HttpGet get = new HttpGet(targetUrl);
		for (String key : httpHeaders.keySet()) {
        	get.setHeader(key, httpHeaders.get(key));
        }
        try {
        	return client.execute(get);
		} catch (UnsupportedEncodingException e) {
//			e.printStackTrace();
		} catch (ClientProtocolException e) {
//			e.printStackTrace();
		} catch (IOException e) {
//			e.printStackTrace();
		}
		return null;
	}

	/**
	 * delete 方法
	 * @param targetUrl
	 * @param httpHeaders
	 */
	public static HttpResponse httpDelete(String targetUrl,Map<String, String> httpHeaders){
		HttpClient client = HttpClients.createDefault();
		HttpDelete delete = new HttpDelete(targetUrl);
		for (String key : httpHeaders.keySet()) {
			delete.setHeader(key, httpHeaders.get(key));
        }
        try {
        	return client.execute(delete);
		} catch (UnsupportedEncodingException e) {
//			e.printStackTrace();
		} catch (ClientProtocolException e) {
//			e.printStackTrace();
		} catch (IOException e) {
//			e.printStackTrace();
		}
		return null;
	}
	
	/**
	 * Head 方法
	 * @param targetUrl
	 * @param httpHeaders
	 */
	public static HttpResponse httpHead(String targetUrl,Map<String, String> httpHeaders){
		HttpClient client = HttpClients.createDefault();
		HttpHead head = new HttpHead(targetUrl);
		for (String key : httpHeaders.keySet()) {
			head.setHeader(key, httpHeaders.get(key));
        }
        try {
        	return client.execute(head);
		} catch (UnsupportedEncodingException e) {
//			e.printStackTrace();
		} catch (ClientProtocolException e) {
//			e.printStackTrace();
		} catch (IOException e) {
//			e.printStackTrace();
		}
		return null;
	}
	
	/**
	 * put 方法
	 * @param targetUrl
	 * @param httpHeaders
	 */
	public static HttpResponse httpPut(String targetUrl,Map<String, String> httpHeaders){
		HttpClient client = HttpClients.createDefault();
		HttpPut put = new HttpPut(targetUrl);
		for (String key : httpHeaders.keySet()) {
			put.setHeader(key, httpHeaders.get(key));
        }
        try {
        	return client.execute(put);
		} catch (UnsupportedEncodingException e) {
//			e.printStackTrace();
		} catch (ClientProtocolException e) {
//			e.printStackTrace();
		} catch (IOException e) {
//			e.printStackTrace();
		}
		return null;
	}
	
	/**
	 * options 方法
	 * @param targetUrl
	 * @param httpHeaders
	 */
	public static HttpResponse httpOptions(String targetUrl,Map<String, String> httpHeaders){
		HttpClient client = HttpClients.createDefault();
		HttpOptions options = new HttpOptions(targetUrl);
		for (String key : httpHeaders.keySet()) {
			options.setHeader(key, httpHeaders.get(key));
        }
        try {
        	return client.execute(options);
		} catch (UnsupportedEncodingException e) {
//			e.printStackTrace();
		} catch (ClientProtocolException e) {
//			e.printStackTrace();
		} catch (IOException e) {
//			e.printStackTrace();
		}
		return null;
	}
	
	/**
	 * 获取response 状态信息
	 * @return
	 */
	public static String getStatusLine(HttpResponse response){
		if(response==null){
			return null;
		}
		return response.getStatusLine().toString();
	}
    
	/**
	 * 获取response 头部
	 * @return
	 */
	public static Map<String, String> getResponseAllHeaders(HttpResponse response){
		if(response==null){
			return null;
		}
		Header headers[] = response.getAllHeaders();  
		Map<String, String> httpHeaders = new HashMap<String, String>();
	    for (int i =0;i < headers.length;i++){    
	       httpHeaders.put(headers[i].getName(), headers[i].getValue());
	    } 
	    return httpHeaders;
	}
	
	/**
	 * 获取响应实体
	 * @return
	 * @throws ParseException
	 * @throws IOException
	 */
	public static String getResponseBody(HttpResponse response) throws ParseException, IOException{
		if(response==null){
			return null;
		}
		HttpEntity httpEntity = response.getEntity();
		return EntityUtils.toString(httpEntity,"UTF-8");
	}
    
//	public static void main(String[] args) {
//		WebUtil hTTPUtil = new WebUtil();
//		try {
//			Map<String, String> httpHeaders = new HashMap<String, String>();
//			httpHeaders.put("Charsert", "UTF-8");
//			httpHeaders.put("Cookies","Hm_lvt_bd81f02e5329554415de9ee15f916a98=1475897340,1476002999");
//			
//	        // 创建一个List容器，用于存放基本键值对（基本键值对即：参数名-参数值）
//			List<BasicNameValuePair> postParameters = new ArrayList<>();
//			postParameters.add(new BasicNameValuePair("name", "张三"));
//			postParameters.add(new BasicNameValuePair("age", "25"));
//	        
//			WebUtil.httpHead("http://127.0.0.1", httpHeaders);
//		} catch (Exception e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//	}
}
