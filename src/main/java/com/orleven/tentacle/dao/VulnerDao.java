package com.orleven.tentacle.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import javax.sql.DataSource;
import com.orleven.tentacle.dao.imp.IVulnerDao;
import com.orleven.tentacle.entity.Vulner;

public class VulnerDao implements IVulnerDao{
	
	/**
	 * 配置数据库
	 */
    private Connection configConnection;
    
	@Override
	public boolean insert(Vulner vulner) {
		
		return true;
	}

	@Override
	public List<Vulner> getAll() {
		List<Vulner> list = new ArrayList<Vulner>();
		try {
			String sql = "Select * from Vulner";
		    Statement smt = configConnection.createStatement();
		    ResultSet rs = smt.executeQuery(sql);
		    while (rs.next()) {
		       int vulnerId = rs.getInt("VulnerId");;
		       String vulnerName = rs.getString("VulnerName");
		       String vulnerDescribe = rs.getString("VulnerDescribe");
		       String repaire = rs.getString("Repaire");
		       String vulnerType = rs.getString("VulnerType");
		       String vulnerRank = rs.getString("VulnerRank");
		       String scriptName = rs.getString("ScriptName");
		       Vulner vulner = new Vulner(vulnerId,vulnerName,vulnerDescribe,repaire,vulnerType,vulnerRank,scriptName);
		       list.add(vulner);
		    }
		       
		} catch (SQLException e) {
			e.printStackTrace();
			return null;
		}

		return list;
	}

	@Override
	public Vulner getVulnerById(int vulnerId) {
		String sql = "SELECT * FROM Vulner WHERE ID = ?";
		try {
			PreparedStatement ps = configConnection.prepareStatement(sql);
			ps.setInt(1, vulnerId);
			Vulner vulner = null;
			ResultSet rs = ps.executeQuery();
			if (rs.next()) {
				vulner = new Vulner(
					rs.getInt("VulnerId"),
					rs.getString("VulnerName"),
					rs.getString("VulnerDescribe"),
					rs.getString("Repaire"),
					rs.getString("VulnerType"),
					rs.getString("VulnerRank"),
					rs.getString("ScriptName")
				);
			}
			rs.close();
			ps.close();
			return vulner;
		} catch (SQLException e) {
			e.printStackTrace();
			return null;
		}
	}

	@Override
	public Vulner getVulnerByCVE(int vulnerCVE) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Vulner getVulnerByName(int vulnerName) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Vulner getVulnerByRank(int vulnerRank) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Vulner getVulnerByType(int vulnerType) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public boolean createTable() throws Exception {
		String sql = "CREATE TABLE 'Vulner' ("
			+ "'VulnerId'  INTEGER NOT NULL,"
			+ "'VulnerName'  TEXT NOT NULL,"
			+ "'VulnerCVE'  TEXT,"
			+ "'VulnerDescribe'  TEXT,"
			+ "'Repaire'  TEXT,"
			+ "'VulnerType'  TEXT NOT NULL,"
			+ "'VulnerRank'  TEXT,"
			+ "'ScriptName'  TEXT NOT NULL,"
			+ "PRIMARY KEY ('VulnerId')"
			+ ");";
		PreparedStatement ps = configConnection.prepareStatement(sql);
		ps.executeUpdate();
		ps.close();
		return true;
	}

}
