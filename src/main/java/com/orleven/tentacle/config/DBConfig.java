package com.orleven.tentacle.config;


import javax.sql.DataSource;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.autoconfigure.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;


/**
 * 数据库配置
 * @author orleven
 * @date 2017年3月8日
 */
@Configuration
public class DBConfig {


	/**
	 * Tentacle 配置存储
	 * @data 2017年3月19日
	 * @return
	 */
	@Bean("configDataSource")
	@Qualifier("configDataSource") 
    public DataSource configDataSource() {
        DataSourceBuilder dataSourceBuilder = DataSourceBuilder.create();
        dataSourceBuilder.driverClassName("org.sqlite.JDBC");
        dataSourceBuilder.url("jdbc:sqlite:config/config.db");
        return dataSourceBuilder.build();
    }
    
    /**
     * Tentacle 重要数据存储
     * @data 2017年3月19日
     * @return
     */
	@Bean("tentacleDataSource")
	@Qualifier("tentacleDataSource") 
	@Primary
    public DataSource tentacleDataSource() {
        DataSourceBuilder dataSourceBuilder = DataSourceBuilder.create();
        dataSourceBuilder.driverClassName("org.sqlite.JDBC");
        dataSourceBuilder.url("jdbc:sqlite:config/tentacle.db");
        return dataSourceBuilder.build();
    }

}
