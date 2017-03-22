package com.orleven.tentacle.util;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.List;

/**
 * 文件处理
 * @author orleven
 * @date 2017年3月8日
 */
public class FileUtil {
	
	/**
	 * 读取文本文件所有内容
	 * @data 2017年3月8日
	 * @param filePath
	 * @return
	 */
    public static String readAll(String filePath){

        try {
            FileReader fr=new FileReader(filePath);
            BufferedReader br=new BufferedReader(fr);
            String res="";
            String buf;
            while((buf=br.readLine())!=null){
                res+=buf;
            }
            br.close();
            fr.close();
            return res;
        }catch (IOException e){
            e.printStackTrace();
        }
        return null;
    }

    /**
     * 按照编码，读取文本文件所有内容
     * @data 2017年3月8日
     * @param path
     * @param charset
     * @return
     */
    public static String readAll(String path,String charset){

        try {
            File file = new File(path);

            if (!file.exists()) {
                return null;
            }

            FileInputStream inputStream = new FileInputStream(file);
            byte[] length = new byte[inputStream.available()];
            inputStream.read(length);
            inputStream.close();
            return new String(length,charset);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return null;
    }

    /**
     * 读取文件的byte,未测试
     * @data 2017年3月8日
     * @param filePath
     * @return
     */
    public static byte[] readByte(String filePath){
        try {
            FileInputStream fis = new FileInputStream(filePath);
            FileChannel channel = fis.getChannel();
            ByteBuffer byteBuffer = ByteBuffer.allocate((int)channel.size());
            while((channel.read(byteBuffer)) > 0){
                // do nothing
//              System.out.println("reading");
            }
            channel.close();
            fis.close();
            return byteBuffer.array();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * 按行读取文件
     * @data 2017年3月8日
     * @param filePath
     * @return
     */
    public static List<String> readLines(String filePath){

        try {
            FileReader fr=new FileReader(filePath);
            BufferedReader br=new BufferedReader(fr);
            List<String> res=new ArrayList<>();
            String buf;
            while((buf=br.readLine())!=null){
                res.add(buf);
            }
            br.close();
            fr.close();
            return res;
        }catch (IOException e){
            e.printStackTrace();
        }
        return null;
    }

    /**
     * 写入文件
     * @data 2017年3月8日
     * @param filePath
     * @param content
     * @param flag 是否追加
     * @return
     */
    public static boolean write(String filePath,String content,boolean flag)
    {
        FileWriter fw;
        BufferedWriter bw;
        try{
            fw=new FileWriter(filePath,flag);
            bw=new BufferedWriter(fw);
            bw.write(content);
            bw.close();
            fw.close();
            return true;
        }catch (IOException e){
            e.printStackTrace();
        }
        return false;
    }
	
	
    /**
     * 删除一个文件下的所有文件或者删除某个文件
     * @data 2017年3月8日
     * @param file
     * @return
     */
	public static boolean deleteAll(File file) {
		while(file.exists()){
			delSub(file);
		}
		return true;
	}
	
	/**
	 * 删除一个文件下的所有文件或者删除某个文件
	 * @data 2017年3月8日
	 * @param file
	 * @return
	 */
	public static boolean delSub(File file){
		try{

			if (file.isFile()|| (file.list()!=null&&file.list().length == 0) ) {
				file.delete();
			} 
			else {
				File[] files = file.listFiles();
				for (int i = 0;  i < files.length; i++) {
					deleteAll(files[i]);
					files[i].delete();
				}
			}
			if (file.exists()) // 如果文件本身就是目录 ，就要删除目录
				file.delete();
		}catch (Exception e) {
			e.printStackTrace();
		}
		return true;
	}
}
