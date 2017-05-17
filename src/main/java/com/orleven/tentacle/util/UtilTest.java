package com.orleven.tentacle.util;

import java.util.List;
import java.util.Map;

/**
 * 用于Util的测试
 * @author orleven
 * @date 2017年5月11日
 */
public class UtilTest {

	public void test() {
		List<Map<String,String>> nodes = XMLUtil.listNodes("config/vulner.xml");
		for(Map<String,String> node:nodes){
			System.out.println("------------------------------------");
			System.out.println("vulnerId:"+node.get("vulnerId"));
			System.out.println("vulnerName:"+node.get("vulnerName"));
			System.out.println("vulnerCVE:"+node.get("vulnerCVE"));
			System.out.println("vulnerDescribe:"+node.get("vulnerDescribe"));
			System.out.println("repaire:"+node.get("repaire"));
			System.out.println("vulnerType:"+node.get("vulnerType"));
			System.out.println("vulnerRank:"+node.get("vulnerRank"));
			System.out.println("scriptName:"+node.get("scriptName"));
			System.out.println("scriptType:"+node.get("scriptType"));
		}
	}
}
