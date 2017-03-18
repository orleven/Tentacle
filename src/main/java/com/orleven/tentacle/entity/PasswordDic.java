package com.orleven.tentacle.entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

/**
 * 密码字典库
 * @author orleven
 * @date 2017年2月23日
 */
@Entity
@Table(name="PasswordDic")
public class PasswordDic {
	
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "Id") 
	private int id;
	
    @Column(name = "Password") 
	private String password;
	
	public PasswordDic(int id,String password){
		this.id = id;
		this.password = password;
	}
	
	public void setId(int id){
		this.id = id;
	}
	
	public int getId(){
		return id;
	}
	
	public String getPassword(){
		return password;
	}
	
	public void setPassword(){
		this.password = password;
	}
}
