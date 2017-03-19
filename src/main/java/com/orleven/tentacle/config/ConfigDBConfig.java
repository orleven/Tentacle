package com.orleven.tentacle.config;

import java.sql.Connection;
import java.sql.SQLException;

import javax.sql.DataSource;

import org.springframework.stereotype.Component;

/**
 * Config 数据库
 * @author orleven
 * @date 2017年3月19日
 */
@Component
public class ConfigDBConfig {

	/**
	 * 配置数据库
	 */
    private DataSource configDataSource;
    
    
	/**
	 * 配置数据库
	 */
    private Connection configConnection;
    
    public ConfigDBConfig(){
    	configDataSource = new DBConfig().configDataSource();
    }
    
    public void setConfigDataSource(DataSource configDataSource) {
        this.configDataSource = configDataSource;
    }
    public DataSource getConfigDataSource() {
        return configDataSource;
    }
	
    public void setConfigConnection(Connection configConnection) {
        this.configConnection = configConnection;
    }
    
    public Connection getConfigConnection() {
        return configConnection;
    }
    
    /**
     * 连接配置数据库
     * @data 2017年3月19日
     * @return
     * @throws Exception
     */
	public boolean connectConfigDB() throws Exception {
    	try {
			this.configConnection = configDataSource.getConnection();
		} catch (SQLException e) {
			e.printStackTrace();
			return false;
		}
    	return true;
		
	}
	
	
	/**
	 * 关闭配置数据库
	 * @data 2017年3月19日
	 * @return
	 * @throws Exception
	 */
	public boolean closeConfigConnection() throws Exception{
		if (configConnection != null) {
			try {
				configConnection.close();
			} catch (SQLException e) {
				return false;
			}
		}
	
		return true;
	}
	
}
