package dssearch.controller;

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DSSearch extends HttpServlet {

	private static final long serialVersionUID = 1L;

	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		
		response.getWriter().write(write_form());
	}

	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().write("Error: POST method not implemented.");
	}
	
	private String write_form(){
		String form="";
		form+="<html>\n";
		form+="<head>\n";
		form+="<center><h1>Dataset Search</h1></center>\n";
		form+="</head>\n";
		form+="<body>\n";
		form+="</body>\n";
		form+="</html>\n";
		return form;
	}
}
