package test;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.rdf.model.Statement;
import org.apache.jena.rdf.model.StmtIterator;
import org.apache.jena.riot.RIOT;

public class VoidReader {

	public void read(InputStream in) {

		RIOT.init();
		Model model = ModelFactory.createDefaultModel();
		model.read(in, null, "TURTLE");

		/*
		 * Reader reader = FileUtils.asUTF8(in);
		 * 
		 * TurtleParser parser = new TurtleParser(reader);
		 * parser.setEventHandler(new Turtle2NTriples(System.out));
		 * 
		 * try { parser.parse(); } catch (ParseException e) { // TODO
		 * Auto-generated catch block e.printStackTrace(); }
		 */

		List<String> vocabularies = new ArrayList<String>();
		List<String> subsets = new ArrayList<String>();
		Map<String, String> subsetTriples = new HashMap<String, String>();

		StmtIterator iter = model.listStatements();
		while (iter.hasNext()) {
			Statement stmt = iter.nextStatement();

			Resource subject = stmt.getSubject(); // sujeito
			Property predicate = stmt.getPredicate(); // predicado
			RDFNode object = stmt.getObject(); // objeto

			if (predicate.getLocalName().toString().equals("vocabulary")) {
				vocabularies.add(object.toString());
			}

			if (predicate.getLocalName().toString().equals("subset")) {
				subsets.add(object.toString());
			}

			if (predicate.getLocalName().toString().equals("triples")) {
				subsetTriples.put(subject.getLocalName(), object.toString());
			}

			System.out.println(subject.getLocalName());
			System.out.println(predicate.getLocalName().toString());
			System.out.println(object.toString());
			System.out.println("\n");

		}
	}

	public static void main(String[] args) throws FileNotFoundException {

		InputStream in = new FileInputStream("/home/joncarv/Doutorado/WS/datosartiumorg.ttl");
		// InputStream in = new FileInputStream("/home/joncarv/Desktop/demografiaataun.ttl");

		VoidReader vr = new VoidReader();
		vr.read(in);
	}

}
