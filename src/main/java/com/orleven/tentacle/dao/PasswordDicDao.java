package com.orleven.tentacle.dao;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import javax.sql.DataSource;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import com.orleven.tentacle.dao.imp.IPasswordDicDao;
import com.orleven.tentacle.entity.PasswordDic;

/**
 * Password 字典model
 * @author orleven
 * @date 2017年3月8日
 */
@Component
@Scope("prototype")
public class PasswordDicDao implements IPasswordDicDao{

	private DataSource dataSource;
	
	public void setDataSource(DataSource dataSource) {
		this.dataSource = dataSource;
	}
	
	@Override
	public List<PasswordDic> getAll() {
		Connection conn;
		List<PasswordDic> list = new ArrayList<PasswordDic>();
		try {
			conn = dataSource.getConnection();
			String sql = "Select id, password from PASSWORDDIC";
		    Statement smt = conn.createStatement();

		    ResultSet rs = smt.executeQuery(sql);
		       
		    while (rs.next()) {
		       int id = rs.getInt("id");
		       String password = rs.getString("password");
		       PasswordDic pass = new PasswordDic(id,password);
		       list.add(pass);
		    }
		       
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return list;
	}

	@Override
	public PasswordDic getPasswordById(int id) {
		String sql = "SELECT * FROM PASSWORDDIC WHERE ID = ?";
		Connection conn = null;
		
		try {
			conn = dataSource.getConnection();
			PreparedStatement ps = conn.prepareStatement(sql);
			ps.setInt(1, id);
			PasswordDic passwordDic = null;
			ResultSet rs = ps.executeQuery();
			if (rs.next()) {
				passwordDic = new PasswordDic(
					rs.getInt("id"),
					rs.getString("password")
				);
			}
			rs.close();
			ps.close();
			return passwordDic;
		} catch (SQLException e) {
			throw new RuntimeException(e);
		} finally {
			if (conn != null) {
				try {
				conn.close();
				} catch (SQLException e) {}
			}
		}
	}

	@Override
	public void insert(PasswordDic passwordDic) {
		String sql = "INSERT INTO PASSWORDDIC " +
				"(password) VALUES (?)";
		Connection conn = null;
		
		try {
			conn = dataSource.getConnection();
			PreparedStatement ps = conn.prepareStatement(sql);
			ps.setString(1, passwordDic.getPassword());
			ps.executeUpdate();
			ps.close();
			
		} catch (SQLException e) {
			throw new RuntimeException(e);
		} finally {
			if (conn != null) {
				try {
					conn.close();
				} catch (SQLException e) {}
			}
		}
	}

}
