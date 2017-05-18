package com.orleven.tentacle.util;

import java.io.FileInputStream;
import java.io.IOException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.Security;
import java.security.spec.InvalidKeySpecException;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.PBEParameterSpec;
import javax.crypto.spec.SecretKeySpec;

import org.bouncycastle.jce.provider.BouncyCastleProvider;

import com.orleven.tentacle.util.FileUtil;

/**
 * Weblogic 解密Util
 * weblogic密码忘记破解方法
 * 获取到weblogic安装目录下的两个文件 SerializedSystemIni.dat、 boot.properties
 * (weblogic8上面两个文件在的bea/user_projects/domains/mydomain 目录下)
 * (welogic10 SerializedSystemIni.dat在bea/user_projects/domains/base_domain/security中)
 * (welogic10 boot.properties在bea/user_projects/domains/base_domain/servers/AdminServer/security中)
 * 加入weblogic.jar （weblogic安装目录中寻找，不同版本有可能不同）文件添加至构建路径，
 * welogic10如果运行还缺少别的类可以把weblogic的/wlserver_10.3/server/lib下的jar都添加到构建路径
 * @author orleven
 * @date 2017年5月11日
 */
public class WeblogicPwd {
	
	public static String decrypt(String ciphertext,String serializedSystemIniPath){
		Security.addProvider(new BouncyCastleProvider());   // 只加载一次
		String cleartext = "";
		
		if (ciphertext.startsWith("{AES}")) {
			ciphertext = ciphertext.replaceAll("^[{AES}]+", "");
			try {
				cleartext = WeblogicPwd.decryptAES(
						serializedSystemIniPath, ciphertext);
			} catch (InvalidKeyException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (NoSuchAlgorithmException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (InvalidKeySpecException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (NoSuchPaddingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (InvalidAlgorithmParameterException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (BadPaddingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (IllegalBlockSizeException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		} else if (ciphertext.startsWith("{3DES}")) {
			ciphertext = ciphertext.replaceAll("^[{3DES}]+", "");
			try {
				cleartext = WeblogicPwd.decrypt3DES(
						serializedSystemIniPath, ciphertext);
			} catch (InvalidKeyException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (NoSuchAlgorithmException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (InvalidKeySpecException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (NoSuchPaddingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (InvalidAlgorithmParameterException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (BadPaddingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (IllegalBlockSizeException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		}
		return cleartext;
	}
	
	public static String decryptAES(String SerializedSystemIni, String ciphertext) throws NoSuchAlgorithmException, InvalidKeySpecException, NoSuchPaddingException, InvalidAlgorithmParameterException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException, IOException {

        byte[] encryptedPassword1 = CodeUtil.base64Decode(ciphertext);
        byte[] salt = null;
        byte[] encryptionKey = null;

        String key = "0xccb97558940b82637c8bec3c770f86fa3a391a56";

        char password[] = new char[key.length()];

        key.getChars(0, password.length, password, 0);

        FileInputStream is = new FileInputStream(SerializedSystemIni);
        try {
            salt = FileUtil.readBytes(is);

            int version = is.read();
            if (version != -1) {
                encryptionKey = FileUtil.readBytes(is);
                if (version >= 2) {
                    encryptionKey = FileUtil.readBytes(is);
                }
            }
        } catch (IOException e) {

        }

        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("PBEWITHSHAAND128BITRC2-CBC");

        PBEKeySpec pbeKeySpec = new PBEKeySpec(password, salt, 5);

        SecretKey secretKey = keyFactory.generateSecret(pbeKeySpec);

        PBEParameterSpec pbeParameterSpec = new PBEParameterSpec(salt, 0);

        Cipher cipher = Cipher.getInstance("PBEWITHSHAAND128BITRC2-CBC");
        cipher.init(Cipher.DECRYPT_MODE, secretKey, pbeParameterSpec);
        SecretKeySpec secretKeySpec = new SecretKeySpec(cipher.doFinal(encryptionKey), "AES");

        byte[] iv = new byte[16];
        System.arraycopy(encryptedPassword1, 0, iv, 0, 16);
        int encryptedPasswordlength = encryptedPassword1.length - 16 ;
        byte[] encryptedPassword2 = new byte[encryptedPasswordlength];
        System.arraycopy(encryptedPassword1, 16, encryptedPassword2, 0, encryptedPasswordlength);
        IvParameterSpec ivParameterSpec = new IvParameterSpec(iv);
        Cipher outCipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        outCipher.init(Cipher.DECRYPT_MODE, secretKeySpec, ivParameterSpec);

        byte[] cleartext = outCipher.doFinal(encryptedPassword2);

        return new String(cleartext, "UTF-8");

    }

    public static String decrypt3DES(String SerializedSystemIni, String ciphertext) throws NoSuchAlgorithmException, InvalidKeySpecException, NoSuchPaddingException, InvalidAlgorithmParameterException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException, IOException {

        byte[] encryptedPassword1 = CodeUtil.base64Decode(ciphertext);
        byte[] salt = null;
        byte[] encryptionKey = null;

        String PW = "0xccb97558940b82637c8bec3c770f86fa3a391a56";

        char password[] = new char[PW.length()];

        PW.getChars(0, password.length, password, 0);

        FileInputStream is = new FileInputStream(SerializedSystemIni);
        try {
            salt = FileUtil.readBytes(is);

            int version = is.read();
            if (version != -1) {
                encryptionKey = FileUtil.readBytes(is);
                if (version >= 2) {
                    encryptionKey = FileUtil.readBytes(is);
                }
            }


        } catch (IOException e) {

        }

        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("PBEWITHSHAAND128BITRC2-CBC");

        PBEKeySpec pbeKeySpec = new PBEKeySpec(password, salt, 5);

        SecretKey secretKey = keyFactory.generateSecret(pbeKeySpec);

        PBEParameterSpec pbeParameterSpec = new PBEParameterSpec(salt, 0);

        Cipher cipher = Cipher.getInstance("PBEWITHSHAAND128BITRC2-CBC");
        cipher.init(Cipher.DECRYPT_MODE, secretKey, pbeParameterSpec);
        SecretKeySpec secretKeySpec = new SecretKeySpec(cipher.doFinal(encryptionKey),"DESEDE");

        byte[] iv = new byte[8];
        System.arraycopy(salt, 0, iv, 0, 4);
        System.arraycopy(salt, 0, iv, 4, 4);

        IvParameterSpec ivParameterSpec = new IvParameterSpec(iv);
        Cipher outCipher = Cipher.getInstance("DESEDE/CBC/PKCS5Padding");
        outCipher.init(Cipher.DECRYPT_MODE, secretKeySpec, ivParameterSpec);

        byte[] cleartext = outCipher.doFinal(encryptedPassword1);
        return new String(cleartext, "UTF-8");

    }
}
