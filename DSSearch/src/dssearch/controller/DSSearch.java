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
		form+="<br><br><br>\n";
		form+="<table align=\"center\">\n";
		form+="<tr>\n";
		form+="<tc><img src=\"LOD_Cloud_Diagram.png\" alt=\"LOD Cloud Diagram\" style=\"width:404px;height:228px;\"></tc>\n";
		form+="</tr>\n";
		form+="<tr>\n";
		form+="<tc>\n";
		form+="<form name=\"search\" action=\"/dssearch\" method=\"post\">\n";	
		form+="<input type=\"text\" size=\"80\" name=\"void\"\"/\">";
		form+="</form>\n";
		form+="</tc>\n";
		form+="</tr>\n";
		form+="</table>";
		form+="</body>\n";
		form+="</html>\n";
		return form;
	}
}
