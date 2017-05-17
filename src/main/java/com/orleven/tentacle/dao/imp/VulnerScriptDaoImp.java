package com.orleven.tentacle.dao.imp;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import javax.sql.DataSource;

import org.springframework.stereotype.Component;

import com.orleven.tentacle.dao.VulnerScriptDao;
import com.orleven.tentacle.entity.VulnerScript;

@Component
public class VulnerScriptDaoImp implements VulnerScriptDao{
	
	/**
	 * 配置数据库
	 */
    private Connection configConnection;
    
	@Override
	public boolean insert(VulnerScript vulner) {
		
		return true;
	}

    public void setConfigConnection(Connection configConnection) {
        this.configConnection = configConnection;
    }
    
    public Connection getConfigConnection() {
        return configConnection;
    }
    
	
	@Override
	public List<VulnerScript> getAll() {
		List<VulnerScript> list = new ArrayList<VulnerScript>();
		try {
			String sql = "Select * from VulnerScript";
		    Statement smt = configConnection.createStatement();
		    ResultSet rs = smt.executeQuery(sql);
		    while (rs.next()) {
		       int vulnerId = rs.getInt("VulnerId");;
		       String vulnerName = rs.getString("VulnerName");
		       String vulnerCVE = rs.getString("VulnerCVE");
		       String vulnerDescribe = rs.getString("VulnerDescribe");
		       String repaire = rs.getString("Repaire");
		       String vulnerType = rs.getString("VulnerType");
		       String vulnerRank = rs.getString("VulnerRank");
		       String scriptName = rs.getString("ScriptName");
		       String scriptType = rs.getString("ScriptType");
		       VulnerScript vulnerScript = new VulnerScript(vulnerId,vulnerName,vulnerCVE,vulnerDescribe, repaire,vulnerType,vulnerRank,scriptName,scriptType);
		       list.add(vulnerScript);
		    }
		       
		} catch (SQLException e) {
			e.printStackTrace();
			return null;
		}

		return list;
	}

	@Override
	public VulnerScript getVulnerById(int vulnerId) {
		String sql = "SELECT * FROM VulnerScript WHERE VulnerId = ?";
		try {
			PreparedStatement ps = configConnection.prepareStatement(sql);
			ps.setInt(1, vulnerId);
			VulnerScript vulnerScript = null;
			ResultSet rs = ps.executeQuery();
			if (rs.next()) {
				vulnerScript = new VulnerScript(
					rs.getInt("VulnerId"),
					rs.getString("VulnerName"),
					rs.getString("VulnerCVE"),
					rs.getString("VulnerDescribe"),
					rs.getString("Repaire"),
					rs.getString("VulnerType"),
					rs.getString("VulnerRank"),
					rs.getString("ScriptName"),
					rs.getString("ScriptType")
				);
			}
			rs.close();
			ps.close();
			return vulnerScript;
		} catch (SQLException e) {
			e.printStackTrace();
			return null;
		}
	}

	@Override
	public VulnerScript getVulnerByCVE(String vulnerCVE) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public VulnerScript getVulnerByName(String vulnerName) {
		String sql = "SELECT * FROM VulnerScript WHERE VulnerName = ?";
		try {
			PreparedStatement ps = configConnection.prepareStatement(sql);
			ps.setString(1, vulnerName);
			VulnerScript vulnerScript = null;
			ResultSet rs = ps.executeQuery();
			if (rs.next()) {
				vulnerScript = new VulnerScript(
					rs.getInt("VulnerId"),
					rs.getString("VulnerName"),
					rs.getString("VulnerCVE"),
					rs.getString("VulnerDescribe"),
					rs.getString("Repaire"),
					rs.getString("VulnerType"),
					rs.getString("VulnerRank"),
					rs.getString("ScriptName"),
					rs.getString("ScriptType")
				);
			}
			rs.close();
			ps.close();
			return vulnerScript;
		} catch (SQLException e) {
			e.printStackTrace();
			return null;
		}
	}

	@Override
	public VulnerScript getVulnerByRank(String vulnerRank) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public VulnerScript getVulnerByType(String vulnerType) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public boolean createTable() throws Exception {
		String sql = "CREATE TABLE 'VulnerScript' ("
			+ "'VulnerId'  INTEGER NOT NULL,"
			+ "'VulnerName'  TEXT NOT NULL,"
			+ "'VulnerCVE'  TEXT,"
			+ "'VulnerDescribe'  TEXT,"
			+ "'Repaire'  TEXT,"
			+ "'VulnerType'  TEXT NOT NULL,"
			+ "'VulnerRank'  TEXT,"
			+ "'ScriptName'  TEXT NOT NULL,"
			+ "'ScriptType'  TEXT NOT NULL,"
			+ "PRIMARY KEY ('VulnerId')"
			+ ");";
		PreparedStatement ps = configConnection.prepareStatement(sql);
		ps.executeUpdate();
		ps.close();
		return true;
	}

}
