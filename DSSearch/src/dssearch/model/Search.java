package dssearch.model;

import java.util.ArrayList;
import java.util.List;

import com.hp.hpl.jena.ontology.OntModel;

public class Search {

	public static List<Entry> execute(OntModel ontVoid, int limit, int offset, String method) {
		List<Entry> result = new ArrayList<>();
		//
		// TODO Implementar a busca e retirar a trecho a seguir
		Entry entry = new Entry();
		entry.url = "http://datahub.io/dataset/rkb-explorer-acm";
		entry.name = "Association for Computing Machinery (ACM) (RKBExplorer)";
		entry.description = "Linked Data version of publications of the Association for Computing Machinery (ACM), along with details of their authors.";
		result.add(entry);
		for (int i = 0; i < 13; i++)
			result.add(entry);
		//
		return result;
	}
}
