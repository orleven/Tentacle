package com.orleven.tentacle.util;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.dom4j.Attribute;
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;

/**
 * XML 文件读取类
 * @author orleven
 * @date 2017年5月17日
 */
public class XMLUtil {
	
	/**
	 * 获取XML所有的一级子节点
	 * @data 2017年5月17日
	 */
	public static List<Map<String,String>> listNodes(String path){

		List<Map<String,String>> nodes = new ArrayList<>();
        SAXReader reader = new SAXReader();  
        Document document;
		try {
			document = reader.read(new File(path));
	        Element root = document.getRootElement();  
	        Iterator<Element> iterator = root.elementIterator();  
	        while(iterator.hasNext()){  
	            Element subElement = iterator.next(); 
	            nodes.add(XMLUtil.listSubNodes(subElement));
	        }       	
		} catch (DocumentException e) {
			e.printStackTrace();
			return null;
		}  
        return nodes;
	}

    /**
     * 不外用，遍历二级子节点
     * @data 2017年5月17日
     * @param elementNode
     * @return
     */
    public static Map<String,String> listSubNodes(Element elementNode){   
        Map<String,String> node = new HashMap();
        Iterator<Element> iterator =elementNode.elementIterator();  
        while(iterator.hasNext()){  
        	Element subElement = iterator.next(); 
            node.put(subElement.getName(), subElement.getText()); 
        }  
        return node;
    }  
    

}
