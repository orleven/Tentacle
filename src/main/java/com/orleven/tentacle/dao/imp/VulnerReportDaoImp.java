package com.orleven.tentacle.dao.imp;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import javax.annotation.Resource;
import javax.sql.DataSource;

import org.springframework.stereotype.Component;

import com.orleven.tentacle.dao.VulnerReportDao;
import com.orleven.tentacle.entity.VulnerReport;

@Component
public class VulnerReportDaoImp implements VulnerReportDao{

	/**
	 * 配置数据库
	 */
    private Connection configConnection;
    
    @Resource(name="tentacleDataSource")
	private DataSource dataSource;
	
    public void setDataSource(DataSource dataSource) {
        this.dataSource = dataSource;
    }
    
    
    public DataSource getDataSource() {
        return this.dataSource ;
    }
    

    public void setConfigConnection(Connection configConnection) {
        this.configConnection = configConnection;
    }
    
    public Connection getConfigConnection() {
        return configConnection;
    }
    
	@Override
	public boolean createTable() {
		try {
			String sql = "CREATE TABLE 'VulnerReport' ("
					+ "'ReportId'  INTEGER NOT NULL,"
					+ "'Host'  TEXT NOT NULL,"
					+ "'Port'  TEXT,"
					+ "'Type'  TEXT,"
					+ "'Index'  TEXT,"
					+ "'VulnerId'  INTEGER NOT NULL,"
					+ "'SendMessage'  TEXT NOT NULL,"
					+ "'ReceiveMessage'  TEXT NOT NULL,"
					+ "'Time'  TEXT NOT NULL,"
					+ "PRIMARY KEY ('ReportId')"
					+ ");";
				PreparedStatement ps = configConnection.prepareStatement(sql);
				ps.executeUpdate();
				ps.close();
		} catch (SQLException e) {
			e.printStackTrace();
		} 
			return true;
	}

	@Override
	public boolean insert(VulnerReport vulnerReport) {
		String sql = "INSERT INTO VulnerReport " +
				"(Host,Port,Type,Index,VulnerId,SendMessage,ReceiveMessage,Time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
		try {
			PreparedStatement ps = configConnection.prepareStatement(sql);
			ps.setString(1, vulnerReport.getHost());
			ps.setString(2, vulnerReport.getPort());
			ps.setString(3, vulnerReport.getType());
			ps.setString(4, vulnerReport.getIndex());
			ps.setInt(5, vulnerReport.getVulnerId());
			ps.setString(6, vulnerReport.getSendMessage());
			ps.setString(7, vulnerReport.getReceiveMessage());
			ps.setString(8, vulnerReport.getTime());
			ps.executeUpdate();
			ps.close();
			
		} catch (SQLException e) {
			e.printStackTrace();
		} 
		return true;
	}

	@Override
	public List<VulnerReport> getAll() {
		List<VulnerReport> list = new ArrayList<VulnerReport>();
		try {
			String sql = "Select * from VulnerReport";
		    Statement smt = configConnection.createStatement();
		    ResultSet rs = smt.executeQuery(sql);
		    while (rs.next()) {
		       int reportId = rs.getInt("ReportId");;
		       String host = rs.getString("Host");
		       String port = rs.getString("Port");
		       String type = rs.getString("Type");
		       String index = rs.getString("Index");
		       int vulnerId = rs.getInt("VulnerId");
		       String sendMessage = rs.getString("SendMessage");
		       String receiveMessage = rs.getString("ReceiveMessage");
		       String time = rs.getString("Time");
		       VulnerReport vulnerReport = new VulnerReport(reportId,host,port,type, index,vulnerId,sendMessage,receiveMessage,time);
		       list.add(vulnerReport);
		    }
		       
		} catch (SQLException e) {
			e.printStackTrace();
			return null;
		}

		return list;
	}

	@Override
	public VulnerReport getReportById(int reportId) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public VulnerReport getReportByVulnerId(String VulnerId) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public VulnerReport getReportByHost(String host) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public VulnerReport getReportByPort(String port) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public VulnerReport getReportByIndex(String index) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public boolean isTableExist() {
		boolean flag = false;
		try {
			String sql = "select * from sqlite_master where type = 'table' and name = 'VulnerReport'";

			PreparedStatement ps = configConnection.prepareStatement(sql);
			
			ResultSet rs = ps.executeQuery();
			if (rs.next()) {
				flag = true;
			}
			rs.close();
			ps.close();
		}catch (SQLException e) {
			return false;
		}
		return flag;
	}


	@Override
	public boolean deleteAll() {
		try {
			String sql = "delete from VulnerReport";
			PreparedStatement ps = configConnection.prepareStatement(sql);
			ps.executeUpdate();
			ps.close();
		}catch (SQLException e) {
			return false;
		}
		return true;

	}


	@Override
	public boolean deleteTable() {
		try {
			String sql = "DROP TABLE VulnerReport;";
			PreparedStatement ps = configConnection.prepareStatement(sql);
			ps.executeUpdate();
			ps.close();
		}catch (SQLException e) {
			return false;
		}
		return true;
	}
	
	@Override
	public boolean connectDB() {
    	try {
			this.configConnection = dataSource.getConnection();
		} catch (SQLException e) {
			e.printStackTrace();
			return false;
		}
    	return true;
		
	}
	
	@Override
	public boolean closeConnection(){
		if (configConnection != null) {
			try {
				configConnection.close();
				return true;
			} catch (SQLException e) {
				
			}
		}
		return false;
	}
	
}
