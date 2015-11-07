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
		String void_ = request.getParameter("void").toString();
		if (void_ == null || void_.equals(""))
			void_ = getVoid(request.getParameter("url").toString());
		OntModel ontVoid = loadVoid(void_);
		List<Entry> result = Search.search(ontVoid, 20, 0, "default");
		response.getWriter().write("");
	}

	private String getVoid(String url) {
		String void_ = "";
		//
		// TODO Carregar descrição Void
		//
		return void_;
	}

	private OntModel loadVoid(String void_) {
		OntModel ontVoid = null;
		//
		// TODO Converter descrição void para modelo Ontologia Jena
		//
		return ontVoid;
	}
}
