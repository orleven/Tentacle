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

	/**
	 * 配置数据库
	 */
    private Connection configConnection;
	
	@Override
	public List<PasswordDic> getAll() {
		List<PasswordDic> list = new ArrayList<PasswordDic>();
		try {
			String sql = "Select id, password from PASSWORDDIC";
		    Statement smt = configConnection.createStatement();

		    ResultSet rs = smt.executeQuery(sql);
		       
		    while (rs.next()) {
		       int id = rs.getInt("id");
		       String password = rs.getString("password");
		       PasswordDic pass = new PasswordDic(id,password);
		       list.add(pass);
		    }
		       
		} catch (SQLException e) {
			e.printStackTrace();
			return null;
		}

		return list;
	}

	@Override
	public PasswordDic getPasswordById(int id) {
		String sql = "SELECT * FROM PASSWORDDIC WHERE ID = ?";
		try {
			PreparedStatement ps = configConnection.prepareStatement(sql);
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
			e.printStackTrace();
			return null;
		}
	}

	@Override
	public boolean insert(PasswordDic passwordDic) {
		String sql = "INSERT INTO PASSWORDDIC " +
				"(password) VALUES (?)";
		try {
			PreparedStatement ps = configConnection.prepareStatement(sql);
			ps.setString(1, passwordDic.getPassword());
			ps.executeUpdate();
			ps.close();
		} catch (SQLException e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}

	@Override
	public boolean createTable() throws Exception {
		String sql = "CREATE TABLE 'PasswordDic' ("
			+ "'Id'  INTEGER NOT NULL,"
			+ "'Password'  TEXT NOT NULL,"
			+ "PRIMARY KEY ('Id')"
			+ ");"	;
		PreparedStatement ps = configConnection.prepareStatement(sql);
		ps.executeUpdate();
		ps.close();
		return true;
	}

}
