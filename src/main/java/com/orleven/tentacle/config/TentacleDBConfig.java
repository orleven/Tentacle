package com.orleven.tentacle.config;

import java.sql.Connection;
import java.sql.SQLException;

import javax.annotation.Resource;
import javax.sql.DataSource;
import org.springframework.stereotype.Component;

/**
 * Tentacle 数据库配置
 * @author orleven
 * @date 2017年3月19日
 */
@Component
public class TentacleDBConfig {
	
	/**
	* 数据数据库
	*/

    @Resource(name="tentacleDataSource")
	private DataSource tentacleDataSource;
	 
	/**
	 * 数据数据库
	 */
	private Connection tentacleConnection;
	
//    public TentacleDBConfig(){
//    	tentacleDataSource = new DBConfig().tentacleDataSource();
//    }
    
//	public void setTentacleDataSource(DataSource tentacleDataSource) {
//		this.tentacleDataSource = tentacleDataSource;
//	}
	    
	    
//	public DataSource getTentacleDataSource() {
//	    return tentacleDataSource;
//	}
	    
	public void setTentacleConnection(Connection tentacleConnection) {
	    this.tentacleConnection = tentacleConnection;
	}
	    
	public Connection getTentacleConnection() {
	    return tentacleConnection;
	}
	    

	/**
	 * 连接重要数据库
	 * @data 2017年3月19日
	 * @return
	 * @throws Exception
	 */
	public boolean connectTentacleDB() throws Exception {
	   	try {
			this.tentacleConnection = tentacleDataSource.getConnection();
		} catch (SQLException e) {
			e.printStackTrace();
			return false;
		}
	   	return true;
	}
	
	/**
	 * 关闭重要数据库
	 * @data 2017年3月19日
	 * @return
	 * @throws Exception
	 */
	public boolean closeTentacleConnection() throws Exception{
		if (tentacleConnection != null) {
			try {
				tentacleConnection.close();
			} catch (SQLException e) {
				return false;
			}
		}
		return true;
	}
}
