package dssearch.controller;

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ShowResult extends HttpServlet {

	private static final long serialVersionUID = 1L;

	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().write("Error: Get method not implemented.");
	}

	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		int limit = (Integer) request.getSession().getAttribute("limit");
		int offset = (Integer) request.getSession().getAttribute("offset");
		String command = (String) request.getParameter("command");
		if (command.equals("next"))
			offset += limit;
		else if (command.equals("previous"))
			offset -= limit;
		else if (command.equals("top"))
			offset = 0;
		offset = offset >= 0 ? offset : 0;
		request.getSession().setAttribute("offset",(Integer)offset);

		request.getRequestDispatcher("result.jsp").forward(request, response);
	}

}
