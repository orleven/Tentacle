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
		String text = WeblogicPwd.decrypt("{AES}YOMuT5kqvSXcaWBRAKClFCGUPaAPQrEcvmAhpfreJ7k=", "C:\\Users\\dell\\Desktop\\SerializedSystemIni.dat");
		System.out.println(text);
	}
	
	
}
