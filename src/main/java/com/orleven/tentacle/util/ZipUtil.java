package com.orleven.tentacle.util;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import net.lingala.zip4j.core.ZipFile;
import net.lingala.zip4j.exception.ZipException;
import net.lingala.zip4j.model.FileHeader;
import net.lingala.zip4j.model.ZipParameters;
import net.lingala.zip4j.util.Zip4jConstants;

/**
 * Zip 处理工具包
 * 需要注意的是如果压缩包里已经存在要添加的文件，会陷入死循环，所以添加之前要先判断一下。
 * @author orleven
 * @date 2017年3月8日
 */
public class ZipUtil {
	

	/**
	 * 添加文件夹到zip中
	 * @param inPath 
	 * @param outPath
	 * @param password
	 * @return
	 */
	public static boolean addFoldInZip(String inPath,String storagePath,String outPath,String password) {
		try {
			ZipFile zipFile = new ZipFile(outPath);  
			ZipParameters parameters = new ZipParameters();       
			parameters.setCompressionMethod(Zip4jConstants.COMP_DEFLATE);         
			parameters.setCompressionLevel(Zip4jConstants.DEFLATE_LEVEL_NORMAL);
			parameters.setRootFolderInZip(storagePath);  ;  
			if(password!=null&&!password.equals("")){
				parameters.setEncryptFiles(true);  
				parameters.setEncryptionMethod(Zip4jConstants.ENC_METHOD_AES);  
				parameters.setAesKeyStrength(Zip4jConstants.AES_STRENGTH_256);  
				parameters.setPassword(password);  
			}
			zipFile.addFolder(inPath, parameters);  		
			return true;
		} catch (ZipException e) {
			e.printStackTrace();
			return false;
		}
	}
	
	
	/**
	 * 添加文件到zip中指定的文件夹中
	 * @param inPath
	 * @param storagePath
	 * @param outPath
	 * @param password
	 * @return
	 */
	public static boolean addFileInZip(String inPath,String storagePath,String outPath,String password) {
		try {

			ZipFile zipFile = new ZipFile(outPath);
			File inFile = new File(inPath);
			ZipParameters parameters = new ZipParameters();
			parameters.setCompressionMethod(Zip4jConstants.COMP_DEFLATE); // set compression method to deflate compression
			parameters.setCompressionLevel(Zip4jConstants.DEFLATE_LEVEL_NORMAL); 
			parameters.setRootFolderInZip(storagePath);  
			if(password!=null&&!password.equals("")){
				parameters.setEncryptFiles(true);  
				parameters.setEncryptionMethod(Zip4jConstants.ENC_METHOD_AES);  
				parameters.setAesKeyStrength(Zip4jConstants.AES_STRENGTH_256);  
				parameters.setPassword(password); 
			}
			zipFile.addFile(inFile, parameters);
			return true;
		} catch (ZipException e) {
			e.printStackTrace();
			return false;
		}
	}
	
	/**
	 * 添加多个文件到zip中指定的文件夹中
	 * @param inPath
	 * @param storagePath
	 * @param outPath
	 * @param password
	 * @return
	 */
	public static boolean addFilesInZip(ArrayList<File> inFiles,String storagePath,String outPath,String password) {
		try {
			ArrayList filesToAdd = new ArrayList();  
			ZipFile zipFile = new ZipFile(outPath);
			ZipParameters parameters = new ZipParameters();
			parameters.setCompressionMethod(Zip4jConstants.COMP_DEFLATE); // set compression method to deflate compression
			parameters.setCompressionLevel(Zip4jConstants.DEFLATE_LEVEL_NORMAL); 
			parameters.setRootFolderInZip(storagePath);  
			if(password!=null&&!password.equals("")){
				parameters.setEncryptFiles(true);  
				parameters.setEncryptionMethod(Zip4jConstants.ENC_METHOD_AES);  
				parameters.setAesKeyStrength(Zip4jConstants.AES_STRENGTH_256);  
				parameters.setPassword(password); 
			}
			zipFile.addFiles(inFiles, parameters);
			return true;
		} catch (ZipException e) {
			e.printStackTrace();
			return false;
		}
	}

	/**
	 * 从zip中删除文件
	 * @param inPath
	 * @param outPath
	 * @param password
	 * @return
	 */
	public static boolean removeFileInZip(String inPath,String storagePath,String password) {
		try {
			ZipFile zipFile = new ZipFile(inPath);
			if (zipFile.isEncrypted()) {  
				zipFile.setPassword(password);  
			}  
			List fileHeaderList = zipFile.getFileHeaders();  
			storagePath = storagePath.replaceAll("\\\\", "/");
			for (int i =fileHeaderList.size() -1; i>0 ; i--) {  
			    FileHeader fileHeader = (FileHeader)fileHeaderList.get(i); 
			    if(fileHeader.getFileName().indexOf(storagePath)==0){
			    	System.out.println("Name: " + fileHeader.getFileName());  
			    	zipFile.removeFile(fileHeader.getFileName());	
			    }
			}  
			return true;
		} catch (ZipException e) {
			e.printStackTrace();
			return false;
		}
	}
	
	/**
	 * 查看压缩包的文件列表
	 * @param inPath
	 * @param password
	 * @return
	 */
	public static boolean getNameFromZip(String inPath,String password) {
		try {
			ZipFile zipFile = new ZipFile(inPath);
			if (zipFile.isEncrypted()) {  
				zipFile.setPassword(password);  
			}  
			List fileHeaderList = zipFile.getFileHeaders();  
			  
			for (int i = 0; i < fileHeaderList.size(); i++) {  
			    FileHeader fileHeader = (FileHeader)fileHeaderList.get(i); 
				System.out.println("************************************************************");  
			    System.out.println("Name: " + fileHeader.getFileName());  
			    System.out.println("Compressed Size: " + fileHeader.getCompressedSize());  
			    System.out.println("Uncompressed Size: " + fileHeader.getUncompressedSize());  
			    System.out.println("CRC: " + fileHeader.getCrc32());  
			    System.out.println("************************************************************");  
			}  
			return true;
		} catch (ZipException e) {
			e.printStackTrace();
			return false;
		}
	}
	
	/**
	 * 解压zip里的所有文件
	 * @param inPath
	 * @param outPath
	 * @param password
	 * @return
	 */
	public static boolean extractZip(String inPath,String outPath ,String password) {
		try {
			ZipFile zipFile = new ZipFile(inPath);
			if (zipFile.isEncrypted()) {  
				zipFile.setPassword(password);  
			}  
			zipFile.extractAll(outPath); 
			System.out.println(password);
			return true;
		} catch (ZipException e) {
//			e.printStackTrace();
			return false;
		}
	}
	
	/**
	 * 解压zip里的文件
	 * @param inPath 
	 * @param storagePath
	 * @param outPath
	 * @param password
	 * @return
	 */
	public static boolean extractFileFromZip(String inPath,String storagePath,String outPath ,String password) {
		try {
			ZipFile zipFile = new ZipFile(inPath);
			if (zipFile.isEncrypted()) {  
				zipFile.setPassword(password);  
			}  
			List fileHeaderList = zipFile.getFileHeaders();  
			storagePath = storagePath.replaceAll("\\\\", "/");
			for (int i =0;i<fileHeaderList.size() ;i++) {  
			    FileHeader fileHeader = (FileHeader)fileHeaderList.get(i); 
			    if(fileHeader.getFileName().indexOf(storagePath)==0){
			    	zipFile.extractFile(fileHeader, outPath);
			    	zipFile.removeFile(fileHeader.getFileName());	
			    }
			}  
			return true;
		} catch (ZipException e) {
			e.printStackTrace();
			return false;
		}
	}
	
    /**
     * 测试zip 压缩算法
     */
    public static void main(String[] args) {
    	System.out.println("Zip压缩／解压缩测试");  
    	
//    	System.out.println("添加文件夹压缩文件");  
//		String inPath = "C:\\Users\\dell\\Desktop\\测试文件";  
//		String outPath = "C:\\Users\\dell\\Desktop\\test.zip";
//		String storagePath = null;
//		String password = "123456";
//    	ZipUtil.addFoldInZip(inPath, storagePath,outPath,password);
    	
//    	System.out.println("添加文件到压缩文件");  
//		String inPath1 = "C:\\Users\\dell\\Desktop\\IEEE_TPDS2003.docx";  
//		String outPath1 = "C:\\Users\\dell\\Desktop\\test.zip";
//		String storagePath1 = null;
//		String password1 = "";
//    	ZipUtil.addFileInZip(inPath1, storagePath1,outPath1,password1);
    	
//    	System.out.println("删除zip的某个文件");  
//		String storagePath2 = "测试文件\\浙江工商大学毕业论文模板201435";  
//		String inPath2 = "C:\\Users\\dell\\Desktop\\test.zip";
//		String password2 = "123456";
//    	ZipUtil.removeFileInZip(inPath2, storagePath2, password2);
    	
//    	System.out.println("查看zip文件中的内容");  
//    	String inPath3 = "C:\\Users\\dell\\Desktop\\test.zip";  
//    	String password3 = "123456";
//    	ZipUtil.getNameFromZip(inPath3,password3);
    	
    	System.out.println("解压压缩文件");  
    	String inPath4 = "C:\\Users\\dell\\Desktop\\www.zip"; 
    	String outPath4 = "C:\\Users\\dell\\Desktop\\"; 
    	String password4 = "123456";
    	
    	List<String> lines = FileUtil.readLines("C:\\Soft\\渗透测试\\dictionary\\500000-passwords.txt");
    	for(int i=0;i<lines.size();i++){
    		password4 = lines.get(i);
    		//System.out.println(password4);
    		ZipUtil.extractZip(inPath4, outPath4, password4);

    		
    	}
    	
//    	System.out.println("解压zip中的某个文件");  
//    	String inPath5 = "C:\\Users\\dell\\Desktop\\test.zip"; 
//    	String outPath5 = "C:\\Users\\dell\\Desktop\\"; 
//    	String password5 = "123456";
//    	String storagePath5 = "测试文件\\浙江工商大学毕业论文模板201435";
//    	ZipUtil.extractFileFromZip(inPath5, storagePath5, outPath5, password5);
    	
    	System.out.println("已经输出！"); 
    }
}
