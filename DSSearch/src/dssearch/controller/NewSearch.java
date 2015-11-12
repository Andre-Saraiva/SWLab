package dssearch.controller;

import java.io.IOException;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.hp.hpl.jena.ontology.OntModel;

import dssearch.model.Entry;
import dssearch.model.Search;

public class NewSearch extends HttpServlet {

	private static final long serialVersionUID = 1L;

	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().write("Error: Get method not implemented.");
	}

	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		OntModel ontVoid = null;
		String void_ = request.getParameter("void").toString();
		if (!(void_ == null || void_.equals("")))
			ontVoid = toOntVoid(void_);
		else
			ontVoid = getOntVoid(request.getParameter("url").toString());
		String method = request.getParameter("method").toString();
		int limit = 10;
		int offset = 0;

		List<Entry> result = Search.execute(ontVoid, limit, offset, method);
		request.getSession().setAttribute("result", result);
		request.getSession().setAttribute("limit", (Integer) limit);
		request.getSession().setAttribute("offset", (Integer) offset);
		request.getRequestDispatcher("result.jsp").forward(request, response);
	}

	private OntModel getOntVoid(String url) {
		OntModel ontVoid = null;
		//
		// TODO Carregar descrição Void
		//
		return ontVoid;
	}

	private OntModel toOntVoid(String void_) {
		OntModel ontVoid = null;
		//
		// TODO Converter descrição void para modelo Ontologia Jena
		//
		return ontVoid;
	}
}
